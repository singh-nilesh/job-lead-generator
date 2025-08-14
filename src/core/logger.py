import os
import re
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from src.constants import Constants

# Cache for per-session logs path (non-Airflow default)
_session_logs_path = None

# --- Helpers ---

def sanitize(name: str) -> str:
    """Remove characters unsafe for file names."""
    return re.sub(r'[^a-zA-Z0-9_\-\.]', '_', name)

def _ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path

def get_session_logs_path(context_str: str | None = None) -> str:
    """
    Determine log directory path:
      - If a context_str is provided, create a subfolder for it.
      - Otherwise, use a per-session folder (date/time).
    """
    global _session_logs_path
    base = Constants.logs_path
    date_path = _ensure_dir(os.path.join(base, datetime.now().strftime('%d-%m-%Y')))

    if context_str:
        return _ensure_dir(os.path.join(date_path, sanitize(context_str)))

    if _session_logs_path is None:
        _session_logs_path = _ensure_dir(
            os.path.join(date_path, datetime.now().strftime('%H:%M:%S'))
        )
    return _session_logs_path

def _derive_pkg_from_path(pathname: str, record_name: str | None = None) -> str:
    """
    Derive a package-like path from a file system path.
    Prefer from 'src/' onward; else fallback to filename or record name.
    """
    try:
        norm = os.path.normpath(pathname or "")
        parts = norm.split(os.sep)
        if "src" in parts:
            i = parts.index("src")
            pkg = ".".join(parts[i:])
            if pkg.endswith(".py"):
                pkg = pkg[:-3]
            return pkg or (record_name or "app")
        base = os.path.splitext(os.path.basename(norm))[0]
        return base or (record_name or "app")
    except Exception:
        return record_name or "app"

# --- Formatter and Filters ---

class SimpleContextFormatter(logging.Formatter):
    """
    Use provided app_context if present; otherwise derive from the package path of the record.
    """
    def format(self, record):
        ctx = getattr(record, "app_context", None)
        if not ctx:
            record.app_context = _derive_pkg_from_path(
                getattr(record, "pathname", "") or "", getattr(record, "name", None)
            )
        return super().format(record)

class FileFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.INFO

class ConsoleFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.INFO

# --- Lazy Logger ---

class LazyLogger:
    def __init__(self, logger_name: str, use_ctx: bool = False):
        self.logger_name = logger_name
        self._logger = None
        self._use_ctx = use_ctx

    def _initialize_logger(self):
        if self._logger is None:
            logs_path = get_session_logs_path()
            file_path = os.path.join(logs_path, f"{self.logger_name}.log")

            logger = logging.getLogger(f"job_generator.{self.logger_name}")
            logger.setLevel(logging.DEBUG)
            logger.propagate = False

            if not logger.handlers:
                formatter = SimpleContextFormatter(
                    fmt='[%(asctime)s] %(app_context)s:%(lineno)d - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )

                # File handler
                try:
                    file_handler = RotatingFileHandler(
                        file_path, maxBytes=10 * 1024 * 1024, backupCount=5
                    )
                    file_handler.setLevel(logging.INFO)
                    file_handler.setFormatter(formatter)
                    file_handler.addFilter(FileFilter())
                    logger.addHandler(file_handler)
                except Exception:
                    # Fall back to console if file handler fails
                    pass

                # Console handler
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.INFO)
                console_handler.setFormatter(formatter)
                console_handler.addFilter(ConsoleFilter())
                logger.addHandler(console_handler)

            self._logger = logger
        return self._logger

    # Proxy methods with optional ctx=...; sets stacklevel so lineno points to caller
    def debug(self, msg, *args, ctx=None, **kwargs):
        kwargs.setdefault("stacklevel", 2)
        extra = kwargs.pop("extra", {})
        extra["app_context"] = f"DAG-> {ctx[1]} - TASK-> {ctx[2]}" if (self._use_ctx and ctx is not None) else None
        self._initialize_logger().debug(msg, *args, extra=extra, **kwargs)

    def info(self, msg, *args, ctx=None, **kwargs):
        kwargs.setdefault("stacklevel", 2)
        extra = kwargs.pop("extra", {})
        extra["app_context"] = f"DAG-> {ctx[1]} - TASK-> {ctx[2]}" if (self._use_ctx and ctx is not None) else None
        self._initialize_logger().info(msg, *args, extra=extra, **kwargs)

    def warning(self, msg, *args, ctx=None, **kwargs):
        kwargs.setdefault("stacklevel", 2)
        extra = kwargs.pop("extra", {})
        extra["app_context"] = f"DAG-> {ctx[1]} - TASK-> {ctx[2]}" if (self._use_ctx and ctx is not None) else None
        self._initialize_logger().warning(msg, *args, extra=extra, **kwargs)

    def error(self, msg, *args, ctx=None, **kwargs):
        kwargs.setdefault("stacklevel", 2)
        extra = kwargs.pop("extra", {})
        extra["app_context"] = f"DAG-> {ctx[1]} - TASK-> {ctx[2]}" if (self._use_ctx and ctx is not None) else None
        self._initialize_logger().error(msg, *args, extra=extra, **kwargs)

    def critical(self, msg, *args, ctx=None, **kwargs):
        kwargs.setdefault("stacklevel", 2)
        extra = kwargs.pop("extra", {})
        extra["app_context"] = f"DAG-> {ctx[1]} - TASK-> {ctx[2]}" if (self._use_ctx and ctx is not None) else None
        self._initialize_logger().critical(msg, *args, extra=extra, **kwargs)

    def exception(self, msg, *args, ctx=None, **kwargs):
        kwargs.setdefault("stacklevel", 2)
        extra = kwargs.pop("extra", {})
        extra["app_context"] = f"DAG-> {ctx[1]} - TASK-> {ctx[2]}" if (self._use_ctx and ctx is not None) else None
        self._initialize_logger().exception(msg, *args, extra=extra, **kwargs)

# --- Predefined Component Loggers ---

scraper_logger = LazyLogger('scraper')
db_logger = LazyLogger('db')
airflow_logger = LazyLogger('airflow', use_ctx=True)

__all__ = ["scraper_logger", "db_logger", "airflow_logger"]


# --- CLI Test ---
if __name__ == "__main__":
    scraper_logger.info("Test info without context")
    airflow_logger.info("Airflow task started", ctx=("dag", "task", "run"))
