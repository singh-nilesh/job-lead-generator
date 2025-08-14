import json
from datetime import datetime, timedelta
import re
import os
import csv
from src.core.models import JobDetails
from src.core.logger import scraper_logger as logger
from src.constants import Constants


def load_json(path='config.json'):
    with open(path) as f:
        return json.load(f)


def get_airflow_context(ctx: dict | None = None) -> list[str] | None:
    """
    Return context:(dag_id, task_id, run_id) from Airflow context.
    Call only from within a running task (or pass ctx=get_current_context()).
    """
    try:
        if ctx is None:
            try:
                from airflow.sdk import get_current_context
                temp_ctx = get_current_context() if callable(get_current_context) else None
            except Exception:
                return None
            
        if temp_ctx is not None and "ti" in temp_ctx:
            ti = temp_ctx["ti"]
            return [ti.run_id, ti.dag_id, ti.task_id]
        if not isinstance(ctx, dict):
            return None
        
        
    except Exception:
        return None


def _extract_posting_date(posted_text):
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


def write_url_to_file(url_list: list[str]) -> str | None:
    """ Save the collected job Details URLs to .txt"""
    file_path = os.path.join(Constants.artifacts_dir, 'links.txt')
    try:
        logger.info(" Writing links to .txt file")
        with open(file_path, 'w') as f:
            for url in url_list:
                f.write(f"{url}\n")
        return file_path
    except Exception:
        logger.exception("Failed to write URLs to file")
        return None
                
                
def save_to_csv(results:list[JobDetails]) -> str | None:
    """ Save the scraped Job details data to .CSV, for arflow-XCom"""
    try:
        file_path = os.path.join(Constants.artifacts_dir, "jobs.csv")
        logger.info("saving records to CSV file")
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['title', 'company', 'location', 'start_date', 'duration', 
                         'stipend', 'apply_by', 'responsibilities', 'skills_required', 
                         'other_requirements', 'perks', 'openings', 'company_description', 
                         'posted_date','company_url', 'url']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for job in results:
                job_dict = job.__dict__.copy()
                for key, value in job_dict.items():
                    if isinstance(value, list):
                        job_dict[key] = ', '.join(value)
                writer.writerow(job_dict)
        logger.info(f"Successfully saved {len(results)} jobs to jobs.csv")
        return file_path
    except Exception:
        logger.exception("Error saving to CSV")
        return None


def load_csv(
    path: str = os.path.join(Constants.artifacts_dir, "jobs.csv")
    ) -> list[JobDetails] | None:
    """ Loads records from csv to list of JobDetails obj."""
    try:
        job_list = []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                job_details = JobDetails(
                    title=row['title'],
                    company=row['company'],
                    location=row['location'],
                    start_date=row['start_date'],
                    duration=row['duration'],
                    stipend=row['stipend'],
                    apply_by=row['apply_by'],
                    responsibilities=row['responsibilities'],
                    skills_required=row['skills_required'],
                    other_requirements=row['other_requirements'],
                    perks=row['perks'],
                    openings=row['openings'],
                    company_description=row['company_description'],
                    posted_date=row['posted_date'],
                    company_url=row['company_url'],
                    url=row['url']
                )
                job_list.append(job_details)
        return job_list
    except Exception:
        logger.exception(f"Error loading CSV from {path}")
        return None
    

# Define which symbols to export
__all__ = ["load_json", "write_url_to_file", "save_to_csv", "load_csv", "get_airflow_context"]
