from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseScraper(ABC):
    """Abstract base class for all job scrapers."""
    
    @abstractmethod
    def scrape(self, keywords: Optional[List[str]] = None, 
               location: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Scrape job listings based on given criteria.
        
        Args:
            keywords: Optional list of job keywords to search for
            location: Optional location filter
            
        Returns:
            List of job listings as dictionaries
        """
        pass