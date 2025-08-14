"""
    scrapers package
This module contains scrapers for various job portals to extract job listings.

Modules:
    internshala/:
        main_scraper.py:
            - Contains InternshalaScraper class for scraping job details
            - Primary interface for extracting job data: scraper..start_scraping()
            
        url_builder.py:
            - Internal utility used by main_scraper
            - Handles URL construction (not directly accessed by users)

"""

from .internshala.scraper import InternshalaScraper

__all__ = [
    "InternshalaScraper"
]