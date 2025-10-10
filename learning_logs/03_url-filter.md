# AIM: Filter Already Scraped URLs AND worker nodes for Parallelism

## Requirements:
1. Filter URLs that have already been scraped to avoid duplicates.

2. After compilation of list of URLs, check if the URL is already scraped, and filter out new links to scrape.
3. Task Parallelization: Use Airflow's parallel task execution to scrape multiple URLs concurrently.
4. Setup 2 worker nodes to run the scraping tasks in parallel.
5. traking the progress of each task using custom logging. is very dificult to implement. mointing same volume to all worker nodes may cause confusion in logging, the logs may be jumbled up or overwritten. therefore it is beeter to use a centralized logging and monitiring solution like ELK stack or Prometheus with Grafana.


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
- Set the `executor` configuration in `airflow.cfg` to `LocalExecutor`, can use the `env` section in you `docker-compose.yaml file`
```yaml
  airflow:
    image: apache/airflow:2.5.1
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
```
- Use the `task_name.expand()` method to create multiple instances of the scraping task, allowing them to run in parallel.
- Good for simple lab experiments on one machine.

**Using CeleryExecutor:**
- Set the `executor` configuration in `airflow.cfg` to `CeleryExecutor`, can use the `env` section in you `docker-compose.yaml file`
```yaml
  airflow:
    image: apache/airflow:2.5.1
    environment:
      - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
      - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
      - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
     command: >
      bash -c "airflow db init &&
               airflow webserver & 
               airflow scheduler"
  redis:
    image: redis:latest
```

- Add worker nodes to your `docker-compose.yaml` file to handle parallel tasks. same as the airflow service but with `command` to start worker
```yaml
  ...
  ...
    command: celery worker
```
- Requires a message broker (Redis or RabbitMQ).
- can Scale workers with: `docker-compose up -d --scale airflow-worker=2`

**Implement Centralized Logging using Grafana + Prometheus**


## Learning Outcomes:
- Understand how to filter out already scraped URLs using a unique identifier. to prevent wasted scraping efforts.
- Make use of Hash functions to generate unique identifiers for job postings. insted of relying solely on job IDs.
- Gain experience in setting up and configuring Airflow for parallel task execution using CeleryExecutor or LocalExecutor.
- Learn how to manage and scale worker nodes to handle concurrent scraping tasks efficiently.
- Understand the benefits and potential bottlenecks of using the `.expand()` method for task parallelization in Airflow.

