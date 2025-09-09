# AIM: Filter Already Scraped URLs AND worker nodes for Parallelism

## Requirements:
1. Filter URLs that have already been scraped to avoid duplicates.

2. After compilation of list of URLs, check if the URL is already scraped, and filter out new links to scrape.
3. Task Parallelization: Use Airflow's parallel task execution to scrape multiple URLs concurrently.
4. Setup 2 worker nodes to run the scraping tasks in parallel.


## Guides and Suggestions:
- Scraped data is stored in MongoDB, with a **unique identifier** - `_id` for each job posting. for identifier use the **job ID at the end of the URL**.
- If planning to expand to other Job Sites, one should consider using a **hash function** to generate a unique identifier for each job posting based on its URL or content.
 ```python
    import hashlib
    key = hashlib.md5(f"{source_name}:{job_id}".encode()).hexdigest()
```
- Use the MongoDB client library (`pymongo`) to check if a job ID already exists in the database.

- use the `task_name.expand()` method to divide the scraping tasks into smaller chunks, allowing Airflow to run them in parallel.
- Note: the `.expand()` method will create **individual tasks for each URL**, which can result in **bottlenecks**.
- Consider declaring a maximum number of parallel tasks to avoid overwhelming the system.
- Use Airflow's **CeleryExecutor** + **worker nodes** OR **LocalExecutor** (same container) to manage parallel task execution.

**Using LocalExecutor:**
- Set the `executor` configuration in `airflow.cfg` to `LocalExecutor`.
- Ensure that the `parallelism` and `dag_concurrency` settings are configured to allow for multiple tasks to run concurrently.
- Use the `task_name.expand()` method to create multiple instances of the scraping task, allowing them to run in parallel.
