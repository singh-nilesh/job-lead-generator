import sys
import time
import requests
from bs4 import BeautifulSoup
from src.core.models import JobDetails
from src.core.exception import CustomException
from src.core.utils import _extract_posting_date
from src.core.logger import scraper_logger as logger

def _scrape_job_details(
    header:dict,
    url:str
    ) -> JobDetails | None:
    """
    Scrape job details from an Internshala job posting URL.
    
    Args:
        header (dict): HTTP headers to use for the request
        url (str): The URL of the job posting to scrape
        
    Returns:
        Optional[JobDetails]: A JobDetails object containing the extracted information,
                             or None if the page returns a 404 status
                             
    Raises:
        CustomException: If a network error occurs or if there's an error during scraping
    """
    try:
        # Add a random delay to avoid rate limiting
        time.sleep(5)
        logger.info(f"init job details Scraping for {url}")
        
        # Send a GET request to the URL
        response = requests.get(url, headers= header)
        
        # Continue to next link incase of 404
        if response.status_code == 404:
            logger.warning(f"404 not found error for {url} - skipping this job")
            return None
        response.raise_for_status()
        logger.info("Got the response from url")
    
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
            job.skills_required = ', '.join([skill.text.strip() for skill in skills_elements])
        
        # other requirements
        other_req_element = soup.select_one('.text-container.additional_detail')
        if other_req_element:
            job.other_requirements = other_req_element.text.strip()
        
        # perks
        perks_elements = soup.select('.perks_heading + .round_tabs_container .round_tabs')
        if perks_elements:
            job.perks = ', '.join([perk.text.strip() for perk in perks_elements])
        
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
            job.posted_date = _extract_posting_date(posted_text)
            
        # Extract Company url if possible.
        company_url = soup.select_one('.website_link a')
        if company_url and company_url.has_attr('href'):
            job.company_url = str(company_url['href'])
        
        return job
        
    except requests.RequestException as e:
        logger.error(f"Network error when accessing {url}: {str(e)}")
        raise CustomException(f"Network error during scraping: {str(e)}", sys)
    except Exception as e:
        logger.error(f"Excepton occured while fetching 'Job Details' from {url}\n: {str(e)}",)
        raise CustomException(f"Error occured during scraping Job details for {url}", sys)
    
    
    
def _get_jobDetails_url(
    header:dict,
    source_url:str,
    base_url:str = "https://internshala.com"
    ) -> list[str]:
    """
    Scrape job listing URLs from an Internshala search results page.
    
    Args:
        header (dict): HTTP headers to use for the request
        source_url (str): The source URL as per config
        base_url (str, optional): The base URL to prepend to relative URLs. Defaults to "https://internshala.com"
    
    Returns:
        List[str]: A list of absolute URLs for individual job listings
        
    Raises:
        CustomException: If network errors occur during scraping or if parsing fails
    """
    try:
        # Add a random delay to avoid rate limiting
        time.sleep(5)
        logger.info(f"init links Scraping \n{source_url}")
        
        # Send a GET request to the URL and soup
        response = requests.get(source_url, headers= header)
        
        # Continue to next link incase of 404
        if response.status_code == 404:
            logger.warning(f"404 not found error for {source_url} - skipping this URL")
            return []
        
        response.raise_for_status()  # Raise an exception for HTTP errors
        logger.info("got response from the source url")
        
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
                full_url = base_url + str(href)
                url_list.append(full_url)
                
        if len(url_list) > 0:
            logger.info("Successfull scraping for links")
            return url_list
        
        else:
            logger.warning(f"recived Empty response from source \n{source_url}")
            return []

    except requests.RequestException as e:
        logger.error(f"Network error when accessing {source_url}: {str(e)}")
        raise CustomException(f"Network error during scraping: {str(e)}", sys)
    except Exception as e:
        logger.error(f"Excepton occured while fetching 'Job urls' from {source_url}\n", e)
        raise CustomException(f"Error occured during scraping Job list for {source_url}")