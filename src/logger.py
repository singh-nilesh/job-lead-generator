import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
import re


# Session management - create once per application run
_session_logs_path = None

def get_session_logs_path():
    global _session_logs_path
    if _session_logs_path is None:
        date = f"{datetime.now().strftime('%d-%m-%Y')}"
        time = f"{datetime.now().strftime('%H:%M:%S')}"
        _session_logs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs", date, time)
        os.makedirs(_session_logs_path, exist_ok=True)
    return _session_logs_path


# Custom formatter to show full package path
class PackagePathFormatter(logging.Formatter):
    def format(self, record):
        pathname = record.pathname
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up to project root
        if pathname.startswith(base_dir):
            relative_path = os.path.relpath(pathname, base_dir)
            # Remove .py extension and convert / to .
            record.package_path = os.path.splitext(relative_path)[0].replace(os.sep, ".")
        else:
            record.package_path = pathname  # Fallback
        return super().format(record)

# Logger Filter
class FileFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.INFO # exclude DEBUG for file

class ConsoleFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG or record.levelno >= logging.ERROR # DEBUG + ERROR or higher to console


# logger config
def setup_logger(logger_name:str):
    """ Configure a logger for a specific component """
    
    # Use the session logs path
    logs_path = get_session_logs_path()
    
    # new file for each logger,
    file_name = f"{logger_name}.log"
    file_path = os.path.join(logs_path, file_name)
    
    # Create logger if it doesn't exist yet - one logger type per run
    logger = logging.getLogger(f'job_generator.{logger_name}')
    
    # Configure for new logger init
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Custom log formatter with full package path
        log_formater = PackagePathFormatter(
            '[ %(asctime)s ] %(package_path)s:%(lineno)d - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5   #keep logs for 5 days
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(log_formater)
        file_handler.addFilter(FileFilter())
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(log_formater)
        console_handler.addFilter(ConsoleFilter())
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# Create pre-configured loggers for main components
scraper_logger = setup_logger('scraper')
db_logger = setup_logger('db')
pipeline_logger = setup_logger('pipeline')

if __name__ == "__main__":
    scraper_logger.debug("Test debug")
    scraper_logger.info("Test info")
    scraper_logger.warning("test warning")
    scraper_logger.error("test exception")
    scraper_logger.critical("test critical")