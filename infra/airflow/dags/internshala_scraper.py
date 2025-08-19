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
    from src.scrapers import InternshalaScraper
    from src.core import ScraperConfig
    
    user_config = ScraperConfig().load_default_cfg()
    scraper = InternshalaScraper(config=user_config)
    
    @task(task_id="filter_urls")
    def filter_url():
        from src.core.utils import get_airflow_context
        context = get_airflow_context()
        """
        This task filtters out visited tasks from list of Job Urls.
        """
        # Compile and scrape source Urls
        logger.info("Compiling Job links to scrape", ctx=context)
        urls = scraper.get_urls()
        logger.info(f" Successfully filter {len(urls)} to scrape")
        return urls
    
    
    @task(task_id="scrape_persist")
    def scrape(urls):
        """
        This task, scrapes Internshala job details and saves them to local .csv, to be used by other tasks.
        """
        # Imports
        from src.core.utils import save_to_csv, get_airflow_context
        
        # inti task context
        context = get_airflow_context()
        
        if urls is None:
            logger.warning("now links recived at task scrape_persist", ctx=context)
        else:
            logger.info("Proceding with scraping the Job Urls", ctx=context)
        
        # scrape the job details
        result = scraper.scrape(urls, limit=5)
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
    filtered_url = filter_url()
    scraped = scrape(filtered_url)


dag_instance = intershala_scraper_pipline()