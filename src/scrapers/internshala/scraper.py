import sys
from src.core.config import ScraperConfig
from src.core.exception import CustomException
from src.core.logger import scraper_logger as logger
from src.core.models import JobDetails
from src.core.utils import save_to_csv
from ._helpers.url_builder import _url_bilder_init
from ._helpers.bf4_client import _get_jobDetails_url, _scrape_job_details


class InternshalaScraper:
    def __init__ (self, config:ScraperConfig, max_page = 1):
        """
        A scraper for extracting job and internship listings from Internshala.
        Args:
            config (ScraperConfig): Configuration object containing search parameters and HTTP settings
            max_page (int, optional): Maximum number of search result pages to scrape. Defaults to 1.
        """
        self.cfg = config
        self.base_url: str = config.internshala_base_urls
        self.header: dict = config.headers
        self.job_links: list[str] = []
        self.results: list[JobDetails] = []
    
                
    def scrape(self, limit:int = -1) -> list[JobDetails]:
        """
        Execute the scraping process to collect job listings.
        
        This method orchestrates the full scraping workflow:
        1. Build search URLs based on configuration
        2. Extract job listing URLs from search results
        3. Scrape detailed information from each job listing
        
        Args:
        limit (int, optional): Maximum number of job listings to scrape. 
            If negative or not provided, all available listings will be scraped. Defaults to -1.
    
        Returns:
            List[JobDetails]: Collection of job details objects containing all extracted information
                             
        Note:
            The method catches KeyboardInterrupt to allow for graceful
            termination of scraping by the user
        """
        try:
            # compiling URL as per Config
            source_urls = _url_bilder_init(self.cfg)
            logger.info("Finished compiling source URL as per Config")
            
            # get job details url
            for url in source_urls:
                urls = _get_jobDetails_url(
                    header = self.header,
                    source_url = url,
                    base_url = self.base_url
                )
                self.job_links.extend(urls)
            logger.info(f"Successfuly collected {len(self.job_links)} job urls from the source")
                
            # scrape Job Details
            for url in self.job_links[:limit if limit > 0 else None]:
                job = _scrape_job_details(
                    header= self.header,
                    url= url,
                )
                if job is not None:
                    self.results.append(job)
                    logger.info(f"finnished compiling details for \n{url}")
    
        except KeyboardInterrupt:
            logger.critical("User terminated process with KeyboardInterrupt")
        finally:
            return self.results
        

if __name__ == "__main__":
    config = ScraperConfig()
    scraper = InternshalaScraper(config=config)
    res = scraper.scrape()
    if len(res) > 1:
        logger.info("Successfully compleated Job details scraping")
        logger.debug("Saving records to CSV")
        save_to_csv(res)
    else:
        logger.warning("Program Ended: unsuccessfull attempt")
    
    
    