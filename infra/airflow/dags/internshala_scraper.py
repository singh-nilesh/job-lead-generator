from dataclasses import asdict
from airflow.decorators import dag, task
from airflow.exceptions import AirflowSkipException, AirflowFailException
from datetime import datetime
from src.core.logger import airflow_logger as logger
import hashlib
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

#Function for using hash as id
def make_id(url: str) -> str:
    """Generate a stable Mongo _id from a URL."""
    return hashlib.md5(url.encode()).hexdigest()

                
@dag(
    dag_id="internshala_scraper_pipeline",
    schedule=None,
    start_date=datetime(2023, 8, 7),
    catchup=False
)

def intershala_scraper_pipline():
    from src.core import ScraperConfig
    user_config = ScraperConfig().load_default_cfg()
    
    @task(task_id="compile")
    def compile_urls():
        """
        This task compiles and scraps Job Urls from the source.
        """
        from src.scrapers import InternshalaScraper
        from src.core.utils import get_airflow_context
        context = get_airflow_context()
        scraper = InternshalaScraper(user_config)
        
        # Compile and scrape source Urls
        logger.info("Compiling Job links to scrape", ctx=context)
        urls = scraper.build_urls()
        if len(urls) > 0:
            logger.info("Successfully collected Target URLs", ctx=context)
            return urls
        else:
            logger.warning("No URLs to scrape, aborting.", ctx=context)
            return None
        
    
    @task(task_id="filter")
    def filter_url(urls):
        """
        Filter out URLs already present in MongoDB.
        Returns only new (not yet stored) URLs.
        """
        if not urls:
            raise AirflowSkipException("No URLs provided to filter task.")
        
        from src.db_services import MongoClient
        from src.core.utils import get_airflow_context

        context = get_airflow_context()
        if context:
            task_id = context[-1]

        # Map each URL to its hash (_id in Mongo)
        url_to_id = {url: make_id(url) for url in urls}
        hashed_ids = list(url_to_id.values())

        # Query existing docs whose _id is in our hash list
        with MongoClient(**mongo_config, task_id=task_id) as db:
            existing_docs = db.find({"_id": {"$in": hashed_ids}})

        existing_ids = {doc["_id"] for doc in existing_docs}

        # Keep only URLs whose hash is not in existing_ids
        new_urls = [url for url, hid in url_to_id.items() if hid not in existing_ids]

        logger.info(
            f"Filter task: total={len(urls)}, existing={len(existing_ids)}, new={len(new_urls)}",
            ctx=context
        )

        if not new_urls:
            raise AirflowSkipException("No new URLs to scrape.")

        return new_urls
    
    
    @task(task_id="scrape_persist")
    def scrape_persist(urls):
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
                
        # Scrape
        jobs = scraper.scrape(urls, limit=5)    
        jobs = [asdict(job) for job in jobs] # store as dict for mongo
        logger.info(f"Successfully scraped {len(jobs)} Jobs", ctx=context)
        
        # make hash ids
        for job in jobs:
            job["_id"] = make_id(job["url"])
            
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
                logger.info(f"Successfully retrived {len(rows)} records from MongoDB, and 1st id is {rows[0]['_id']} and hash for url is {make_id(rows[0]['url'])}", ctx=context)
            else:
                logger.error("Error retriving the records.", ctx=context)
            
            
            
        
        
        
    
    # Task chaining
    raw_url = compile_urls()
    filter = filter_url(raw_url)
    scraped = scrape_persist(filter)
    retrive_task = retrive()
    
    raw_url.set_downstream(filter)
    filter.set_downstream(scraped)
    scraped.set_downstream(retrive_task)
    


dag_instance = intershala_scraper_pipline()