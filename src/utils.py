import json
from datetime import datetime, timedelta
import re
import csv
from src.scrapers.models import JobDetails


def load_json(path='config.json'):
    with open(path) as f:
        return json.load(f)


def extract_posting_date(posted_text):
    """
    Extract the actual posting date from various text formats like:
    """
    today = datetime.now().date()
    
    # Case 1: "n day/s ago"
    day_match = re.search(r'Posted (\d+) day', posted_text)
    if day_match:
        days_ago = int(day_match.group(1))
        posted_date = today - timedelta(days=days_ago)
        return posted_date.strftime('%Y-%m-%d')
    
    # Case 2: "few hours ago" or "n hour/s ago"
    elif "hour" in posted_text:
        return today.strftime('%Y-%m-%d')  # Today's date
    
    # Case 3: "n week/s ago"
    week_match = re.search(r'Posted (\d+) week', posted_text)
    if week_match:
        weeks_ago = int(week_match.group(1))
        days_ago = weeks_ago * 7  # Convert weeks to days
        posted_date = today - timedelta(days=days_ago)
        return posted_date.strftime('%Y-%m-%d')
    
    # Additional case: "Posted today"
    elif "today" in posted_text.lower():
        return today.strftime('%Y-%m-%d')
    
    # Additional case: "Posted yesterday"
    elif "yesterday" in posted_text.lower():
        yesterday = today - timedelta(days=1)
        return yesterday.strftime('%Y-%m-%d')
    
    # If no pattern matches, return the original text
    return posted_text


def write_url_to_file(url_list: list[str]):
    """
    This file saves scraped links to .txt file
    """
    with open("links.txt", 'w') as f:
        for url in url_list:
            f.write(f"{url}\n")
                
def save_to_csv(results:list[JobDetails]):
        """
        This fuction saves progress incase of runtime error / keyboard inturrupt
        """
        #logging.info("saving records to CSV file")
        with open("jobs.csv", 'w', newline='', encoding='utf-8') as f:
            
            # Define fieldnames based on JobDetails attributes
            fieldnames = ['title', 'company', 'location', 'start_date', 'duration', 
                         'stipend', 'apply_by', 'responsibilities', 'skills_required', 
                         'other_requirements', 'perks', 'openings', 'company_description', 
                         'posted_date','company_url', 'url']
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for job in results:
                # Convert lists to strings for CSV compatibility
                job_dict = job.__dict__.copy()
                for key, value in job_dict.items():
                    if isinstance(value, list):
                        job_dict[key] = ', '.join(value)
                
                writer.writerow(job_dict)
        #logging.info(f"Successfully saved {len(results)} jobs to jobs.csv")
