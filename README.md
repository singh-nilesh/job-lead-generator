# 🧪 DataOps Test Lab – Job Lead Generation System

This repository contains a DataOps test lab for a job lead generation system. It is designed to help you understand how to set up and manage data pipelines, automate workflows, and ensure data quality in a real-world scenario. It also covers various DevOps practices such as CI/CD, monitoring, cloud, and logging.

## Learning Objectives
1. **Build a python scraper for Intershala**
    - <a href="./learning_logs/01_python_scraper.md">Learning log</a> | <a href="https://github.com/singh-nilesh/job-lead-generator/tree/39eb5abd3f30a0be8db09784b2bf155bdd0357e2">Source code</a>

2. **Integrate the scraper with Apache Airflow for scheduling and monitoring**
    - <a href="./learning_logs/02_scraper-airflow.md">Learning log</a> | <a href="">Source code</a>



## Setup Instructions
Pre-requisites:
- Docker and Docker Compose installed on your machine.
- Python 3.8 or higher installed.

### Step 1: Clone the Repository
```bash
# Clone the repository to your local machine
git clone https://github.com/singh-nilesh/job-lead-generator.git
cd job-lead-generator
git checkout <commit-hash>
```
- Replace `<commit-hash>` with the specific commit you want to work with. Visit the Source code links above, the commit-hash will be visible in the URL or the Branch name.

### Step 2: Set Up Docker Compose
```bash
# Run the pre-docker-compose script
./z-pre-docker-compose.sh

# Start the Docker containers using Docker Compose
docker-compose up --build
```