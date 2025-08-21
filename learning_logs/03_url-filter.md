# AIM: Filter Already Scraped URLs AND True Parallelism

## Requirements:
1. Filter URLs that have already been scraped to avoid duplicates.
2. After compilation of list of URLs, check if the URL is already scraped, and filter out new links to scrape.
3. Task Parallelization: Use Airflow's parallel task execution to scrape multiple URLs concurrently.
4. Setup 2 worker nodes to run the scraping tasks in parallel.


## Guides and Suggestions:
- Scraped data is stored in MongoDB, with a **unique identifier** for each job posting. The identifier is the **job ID at the end of the URL**.
- Use the MongoDB client library (`pymongo`) to check if a job ID already exists in the database.

- use the `task_name.expand()` method to divide the scraping tasks into smaller chunks, allowing Airflow to run them in parallel.
- Note: the `.expand()` method will create **individual tasks for each URL**, which can result in **bottlenecks**.
- Consider declaring a maximum number of parallel tasks to avoid overwhelming the system.
