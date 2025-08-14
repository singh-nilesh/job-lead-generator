"""
    core package
    
This package contains core functionality and utilities shared across the job-lead-generator application.

Modules:
    config.py:
        - ScraperConfig: Configuration class for scraper settings
        - Handles parameters like roles, locations, experience requirements
    
    exception.py:
        - CustomException: Custom exception handling for application errors
        - Provides consistent error logging and traceability
    
    logger.py:
        - Logging configuration and setup
        - Provides scraper_logger for consistent logging across modules
    
    models.py:
        - JobDetails: Data model for storing job information
        - Contains fields for job attributes (title, company, location, etc.)
    
    utils.py:
        - extract_posting_date: Utility to parse posting dates from text
        - save_to_csv: Function to save JobDetails objects to CSV files
        - Other helper functions used throughout the application
"""

from .config import ScraperConfig
from .exception import CustomException
from .models import JobDetails
from . import utils
from . import logger

__all__ = [
    "ScraperConfig",
    "CustomException", 
    "JobDetails",
    "utils",
    "logger"
]