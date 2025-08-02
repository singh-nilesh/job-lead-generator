import logging
import os
import re
from datetime import datetime
from logging.handlers import RotatingFileHandler
from src.constants import Constants

# Handle Airflow import gracefully
try:
    from airflow import get_current_context
except ImportError:
    get_current_context = None  # For CLI or testing mode

# Cache for non-Airflow session path
_session_logs_path = None


# --- Helpers ---

def sanitize(name: str) -> str:
    """Remove characters unsafe for file names"""
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

def get_session_logs_path(dag_id=None, task_id=None, run_id=None):
    """Determine log directory path based on Airflow context (or fallback)"""
    global _session_logs_path
    date = datetime.now().strftime('%d-%m-%Y')
    date_path = os.path.join(Constants.logs_path, date)

    if not all([dag_id, task_id]):
        if _session_logs_path is None:
            time = datetime.now().strftime('%H-%M-%S')
            _session_logs_path = os.path.join(date_path, time)
            os.makedirs(_session_logs_path, exist_ok=True)
        return _session_logs_path

    run_folder = sanitize(run_id or f"run_{datetime.now().strftime('%H%M%S')}")
    dag_id_str = sanitize(str(dag_id)) if dag_id else "unknown_dag"
    task_id_str = sanitize(str(task_id)) if task_id else "unknown_task"
    task_path = os.path.join(date_path, run_folder, dag_id_str, task_id_str)
    os.makedirs(task_path, exist_ok=True)
    return task_path

# --- Formatter and Filters ---

class AirflowContextFormatter(logging.Formatter):
    def format(self, record):
        try:
            if callable(get_current_context):
                context = get_current_context()
                if isinstance(context, dict):
                    setattr(record, 'dag_id', context.get('dag_id', 'unknown_dag'))
                    setattr(record, 'task_id', context.get('task_id', 'unknown_task'))
                    setattr(record, 'run_id', context.get('run_id', 'unknown_run'))
                else:
                    setattr(record, 'dag_id', getattr(context, 'dag_id', 'unknown_dag'))
                    setattr(record, 'task_id', getattr(context, 'task_id', 'unknown_task'))
                    setattr(record, 'run_id', getattr(context, 'run_id', 'unknown_run'))
                record.airflow_context = f"{getattr(record, 'dag_id', 'unknown_dag')}.{getattr(record, 'task_id', 'unknown_task')}"
            else:
                record.airflow_context = "non_airflow"
        except Exception:
            record.airflow_context = "non_airflow"
        return super().format(record)

class FileFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.INFO

class ConsoleFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG or record.levelno >= logging.ERROR

# --- Lazy Logger ---

class LazyLogger:
    def __init__(self, logger_name):
        self.logger_name = logger_name
        self._logger = None

    def _get_airflow_context(self):
        try:
            if callable(get_current_context):
                context = get_current_context()
                if isinstance(context, dict):
                    return {
                        'dag_id': context.get('dag_id'),
                        'task_id': context.get('task_id'),
                        'run_id': context.get('run_id')
                    }
                else:
                    return {
                        'dag_id': getattr(context, 'dag_id', None),
                        'task_id': getattr(context, 'task_id', None),
                        'run_id': getattr(context, 'run_id', None)
                    }
        except Exception:
            pass
        return {'dag_id': None, 'task_id': None, 'run_id': None}

    def _initialize_logger(self):
        if self._logger is None:
            context = self._get_airflow_context()
            logs_path = get_session_logs_path(
                dag_id=context['dag_id'],
                task_id=context['task_id'],
                run_id=context['run_id']
            )

            file_name = f"{self.logger_name}.log"
            file_path = os.path.join(logs_path, file_name)

            logger_id = (
                f"job_generator.{context['dag_id']}.{context['task_id']}.{self.logger_name}"
                if context['dag_id'] and context['task_id']
                else f"job_generator.{self.logger_name}"
            )

            logger = logging.getLogger(logger_id)
            logger.setLevel(logging.DEBUG)
            logger.propagate = False  # Prevent duplication in root logger

            if not logger.handlers:
                formatter = AirflowContextFormatter(
                    fmt='[%(asctime)s] %(airflow_context)s:%(lineno)d - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )

                # File handler
                file_handler = RotatingFileHandler(
                    file_path, maxBytes=10 * 1024 * 1024, backupCount=5
                )
                file_handler.setLevel(logging.INFO)
                file_handler.setFormatter(formatter)
                file_handler.addFilter(FileFilter())

                # Console handler
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.DEBUG)
                console_handler.setFormatter(formatter)
                console_handler.addFilter(ConsoleFilter())

                logger.addHandler(file_handler)
                logger.addHandler(console_handler)

            self._logger = logger
        return self._logger

    # Proxy methods
    def debug(self, msg, *args, **kwargs):
        self._initialize_logger().debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._initialize_logger().info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._initialize_logger().warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._initialize_logger().error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._initialize_logger().critical(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self._initialize_logger().exception(msg, *args, **kwargs)

# --- Predefined Component Loggers ---

scraper_logger = LazyLogger('scraper')
db_logger = LazyLogger('db')
airflow_logger = LazyLogger('airflow')

# --- CLI Test ---
if __name__ == "__main__":
    scraper_logger.debug("Test debug from CLI")
    scraper_logger.info("Test info from CLI")
    scraper_logger.warning("Test warning from CLI")
    scraper_logger.error("Test error from CLI")
    scraper_logger.critical("Test critical from CLI")
