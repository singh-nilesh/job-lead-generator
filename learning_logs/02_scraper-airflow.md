# AIM: Data Pipeline Integration

## Requirements:
1. Integrate the Python scraper with **Apache Airflow** to automate the scraping process.
2. Create an Airflow **DAG** that runs the scraper at scheduled intervals.
3. Use Airflow's logging and monitoring features to track the scraping process.
4. Use **Docker-compose** to set up the Airflow environment.
5. Store the scraped data in a database (**MongoDB**) instead of a CSV file. don't use the default mongo user, use **pre-defined user and collections**.

## Guides and Suggestions:
- Use the Airflow **PythonOperator** OR **Airflow API**  to run the scraper function.
- Use Airflow's **XCom** feature to pass data between tasks if needed.
- Set up Airflow's **logging** to capture logs from the scraper.
- Use **Docker-compose** to define services for Airflow and MongoDB, ensuring they can communicate.
- Use a MongoDB client library (like `pymongo`) in your scraper to save the scraped data directly to MongoDB.

## Learning Outcomes:
- How to set up and manage Airflow DAGs for scheduled tasks.
- Airflow's architecture and how to use it for data pipelines. It parallels the scraping process.
- How to use combination of `Docker-compose` , `Dockerfile` and **bash init scripts** to configure and manage access rights, file permissions, and environment variables.
- Secrets management and safe practices for storing sensitive information like database credentials.
- Mongo Client, and how to interact with **MongoDB** from Python.
- Using **Base Class(interfaces)** and inheritance to create a modular and **reusable scraper, db_services** architecture.
- Proper Docstings, and exporting public methods and attributes for better maintainability and abstraction (**__ init __.py**). 
- How to use Airflow's monitoring features to track the status of your scraping tasks.
- Standard practices for dataclasses and type hints in Python for better code clarity and maintainability.
- Accommodating project structure for add other scrapers in the future, and how to extend the Airflow DAG to include them.

## references:
- [Airflow - Tasks](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html)