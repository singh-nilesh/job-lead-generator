from dataclasses import asdict
from airflow.decorators import dag, task
from airflow.exceptions import AirflowSkipException, AirflowFailException
from datetime import datetime
from src.core.logger import airflow_logger as logger
import os
import dotenv

# load .env variables
dotenv.load_dotenv()
mongo_config = {
    "user_name": os.environ["APP_USER"],
    "password": os.environ["APP_PASSWORD"],
    "db_name": "jobs",
    "collection_name": 'job_details',  # mongo/init
    "service": "mongo_db"  # from docker-compose file
}
                
@dag(
    dag_id="internshala_scraper_pipeline",
    schedule=None,
    start_date=datetime(2023, 8, 7),
    catchup=False
)

def intershala_scraper_pipline():
    from src.core import ScraperConfig
    user_config = ScraperConfig().load_default_cfg()
    
    @task(task_id="scrape_persist")
    def scrape_persist():
        """
        This task, scrapes Internshala job details and saves them to MongoDb.
        """
        # Imports
        from src.core.utils import get_airflow_context
        from src.scrapers import InternshalaScraper
        from src.db_services import MongoClient
        
        # inti task context & scraper
        context = get_airflow_context()
        scraper = InternshalaScraper(user_config)
        logger.info("Finished init for IntershalaScraper", ctx=context)
        
        # Compile Urls
        urls = scraper.build_urls()
        if not urls:
            logger.warning("No Urls to scrape, Aborting the pipline", ctx=context)
            raise AirflowSkipException("No URLS to scrape")
        logger.info(f"SUccessfully compiled {len(urls)} Job urls", ctx=context)
        
        # Scrape
        jobs = scraper.scrape(urls, limit=5)
        jobs = [asdict(job) for job in jobs] # store as dict for mongo
        logger.info(f"Successfully scraped {len(jobs)} Jobs", ctx=context)
        
        # Mongo persist
        with MongoClient(**mongo_config) as db:
            ids = db.insert(jobs)
            if ids:
                logger.info(f"Finnised inserting {len(ids)} records MongoDB", ctx=context)
            else:
                logger.error(f"Error occured wile inserting record, refer to db_log", ctx=context)
    
    
    @task(task_id="retrive")
    def retrive():
        """
        This Task checks if data was inserted correctly
        """
        from src.db_services import MongoClient
        from src.core.utils import get_airflow_context
        
        context = get_airflow_context()
        
        logger.info("Retriving records from MongoDB", ctx=context)
        with MongoClient(**mongo_config) as db:
            rows = db.find()
            if rows:
                logger.info(f"Successfully retrived {len(rows)} records from MongoDB, and 1st id is {rows[0]["_id"]}", ctx=context)
            else:
                logger.error("Error retriving the records.", ctx=context)
            
            
            
        
        
        
    
    # Task chaining
    scraped = scrape_persist()
    select = retrive()
    
    # Enforcing order manually, as there is no dependdency as of now
    scraped.set_downstream(select)


dag_instance = intershala_scraper_pipline()