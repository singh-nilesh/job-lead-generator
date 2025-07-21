import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
from src.config import ScraperConfig
import csv
from src.exception import CustomException
from src.logger import logging
from src.scrapers.internshala import url_builder
from src.scrapers.models import JobDetails
from src.utils import extract_posting_date


class InternshalaScraper:
    def __init__ (self, config:ScraperConfig, max_page = 1):
        self.cfg = config
        self.max_pages = max_page
        self.timeout = config.timeout
        self.base_url: str = config.internshala_base_urls
        self.header: str = config.headers
        self.job_links: list[str] = []
        self.results: list[JobDetails] = []
    
    def _write_url_to_file(self, url_list: list[str]):
        with open("links.txt", 'w') as f:
            for url in url_list:
                f.write(f"{url}\n")
                
                
    def start_scraping(self) -> bool:
        """Main controller"""
        try:
            # compiling URL as per Config
            source_urls = self._url_builder()
            
            # get job details url
            for url in source_urls:
                self._get_jobDetails_url(url)
            self._write_url_to_file(self.job_links)
            
            # scrape Job Details
            for url in self.job_links:
                self._scrape_job_details(url)
            
            if len(self.results) > 0:
                logging.info(f"Successfully scraped {len(self.results)} jobs on {datetime.now().date()}")
                return True
            else:
                logging.info(f"Unsuccessfull attempt: no jobs scraped on {datetime.now().date()}")
                return False
    
        except KeyboardInterrupt:
            logging.info("User terminated process with KeyboardInterrupt")
            self._save_progress()
            return False
        
        
    def _url_builder(self) -> list[str]:
        """This function compiles source urls for internships and jobs"""
        url_list = []
        if self.cfg.internship :
            url_list.append(url_builder.build_internship_url(self.cfg))
        
        if self.cfg.job:
            url_list.append(url_builder.build_job_url(self.cfg))
        
        logging.info(f"Compiled url \n {url_list}")
        return url_list
        
        
    def _scrape_job_details(self, url:str):
        """Scrape job details from an Internshala job posting."""
        try:
            # Add a random delay to avoid rate limiting
            time.sleep(5)
            logging.info(f"init job details Scraping {url}")
            
            # Send a GET request to the URL
            response = requests.get(url, headers=self.header)
            response.raise_for_status()
            logging.info("Got the response from url")
        
            # Parse the BeautifulSoup constructor
            soup = BeautifulSoup(response.content, 'html.parser')
            job = JobDetails()
            job.url = url
            
            # job tile
            title_element = soup.select_one('.heading_4_5.profile')
            if title_element:
                job.title = title_element.text.strip()
        
            # company name
            company_element = soup.select_one('.company_and_premium a')
            if company_element:
                job.company = company_element.text.strip()

            # location
            location_element = soup.select_one('#location_names span')
            if location_element:
                job.location = location_element.text.strip()

            # start date
            start_date_element = soup.select_one('#start-date-first')
            if start_date_element:
                job.start_date = start_date_element.text.strip()

            # duration
            duration_elements = soup.select('.item_body')
            for elem in duration_elements:
                if 'Month' in elem.text:
                    job.duration = elem.text.strip()
                    break
                
            # stipend
            stipend_element = soup.select_one('.stipend')
            if stipend_element:
                job.stipend = stipend_element.text.strip()

            # apply by date
            apply_by_elements = soup.select('.item_body')
            for elem in apply_by_elements:
                if "'" in elem.text and len(elem.text.strip()) < 15:
                    job.apply_by = elem.text.strip()
                    break
                
            # responsibilities
            responsibilities_element = soup.select_one('.about_heading + .text-container')
            if responsibilities_element:
                job.responsibilities = responsibilities_element.text.strip()

            # skills required
            skills_elements = soup.select('.skills_heading + .round_tabs_container .round_tabs')
            if skills_elements:
                job.skills_required = [skill.text.strip() for skill in skills_elements]

            # other requirements
            other_req_element = soup.select_one('.text-container.additional_detail')
            if other_req_element:
                job.other_requirements = other_req_element.text.strip()

            # perks
            perks_elements = soup.select('.perks_heading + .round_tabs_container .round_tabs')
            if perks_elements:
                job.perks = [perk.text.strip() for perk in perks_elements]

            # number of openings
            openings_element = soup.select_one('.section_heading:-soup-contains("Number of openings") + .text-container')
            if openings_element:
                job.openings = openings_element.text.strip()

            # company description
            company_desc_element = soup.select_one('.text-container.about_company_text_container')
            if company_desc_element:
                job.company_description = company_desc_element.text.strip()

            # Extract posted date (from text like "Posted 1 day ago")
            posted_date_element = soup.select_one('.status.status-success')
            if posted_date_element:
                posted_text = posted_date_element.text.strip()
                job.posted_date = extract_posting_date(posted_text)
            
            logging.info(f"finnished compiling details for \n{url}")
            self.results.append(job)

        except Exception as e:
            raise CustomException(f"Error occured during scraping Job details for {url}")

        
    def _get_jobDetails_url(self, source_url:str):
        try:
            """
            This fumction scrapes urls for list of jobs
            """
            # Add a random delay to avoid rate limiting
            time.sleep(5)
            logging.info(f"init links Scraping \n{source_url}")
            
            # Send a GET request to the URL and soup
            response = requests.get(source_url, headers= self.header)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logging.info("got response from the source url")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all job listings
            job_listings = soup.select('div.container-fluid.individual_internship')
            
            # Extract job URLs from each listing
            url_list = []
            for job in job_listings:
                job_link = job.select_one('a.job-title-href')
                if job_link and job_link.has_attr('href'):
                    
                    # Get the href attribute and append it to the base URL
                    href = job_link['href']
                    full_url = self.base_url + href
                    url_list.append(full_url)
                    
            if len(url_list) > 0:
                logging.info("Successfull scraping for links")
                self.job_links.extend(url_list)
            else:
                logging.info(f"ERROR : recived Empty response from source \n{source_url}")

        except :
            raise CustomException(f"Error occured during scraping Job list for {source_url}")
                
    
    def _save_progress(self):
        """
        This fuction saves progress incase of runtime error / keyboard inturrupt
        """
        logging.info("saving records to CSV file")
        with open("jobs.csv", 'w', newline='', encoding='utf-8') as f:
            
            # Define fieldnames based on JobDetails attributes
            fieldnames = ['title', 'company', 'location', 'start_date', 'duration', 
                         'stipend', 'apply_by', 'responsibilities', 'skills_required', 
                         'other_requirements', 'perks', 'openings', 'company_description', 
                         'posted_date', 'url']
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for job in self.results:
                # Convert lists to strings for CSV compatibility
                job_dict = job.__dict__.copy()
                for key, value in job_dict.items():
                    if isinstance(value, list):
                        job_dict[key] = ', '.join(value)
                
                writer.writerow(job_dict)
        logging.info(f"Successfully saved {len(self.results)} jobs to jobs.csv")



if __name__ == "__main__":
    config = ScraperConfig()
    scraper = InternshalaScraper(config=config)
    res = scraper.start_scraping()
    if res:
        logging.info("Successfully compleated Job details scraping")
        scraper._save_progress()
    else:
        logging.error("Program Ended: unsuccessfull attempt")