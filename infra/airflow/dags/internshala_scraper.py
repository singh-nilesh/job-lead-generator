from airflow.decorators import dag, task
from datetime import datetime
from src.core.logger import airflow_logger as logger
                
@dag(
    dag_id="internshala_scraper_pipeline",
    schedule=None,
    start_date=datetime(2023, 8, 7),
    catchup=False
)

def intershala_scraper_pipline():
    
    @task(task_id="scrape_&_save")
    def scrape():
        """
        This task, scrapes Internshala job details and saves them to local .csv, to be used by other tasks.
        """
        # Imports
        from src.scrapers import InternshalaScraper
        from src.core import ScraperConfig
        from src.core.utils import save_to_csv, get_airflow_context
        
        # inti task context
        context = get_airflow_context()
        
        config = ScraperConfig()
        scraper = InternshalaScraper(config= config)
        
        # scrape the job details
        logger.info("inti Scraping Internshala job Urls", ctx=context)
        result = scraper.scrape(limit=5)
        logger.info(f"Successfuly scraped {len(result)} jobs.", ctx=context)
        
        # Temporary storage in .csv
        logger.info("Saving scraped data to jobs.csv foe temporary storage.", ctx=context)
        csv_file_path = save_to_csv(result)
        if csv_file_path:
            logger.info("Successfuly saved to .csv", ctx=context)
            return csv_file_path
        else:
            logger.info("failed at saving to jobs.csv", ctx=context)
            return
    
    # Task chaining
    scraped = scrape()


dag_instance = intershala_scraper_pipline()