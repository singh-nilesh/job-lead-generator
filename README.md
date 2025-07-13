# 🧪 DataOps Test Lab – Job Lead Generation System

**"AI-Powered Job Lead Generation & Contact Discovery Platform"**

This system scrapes job portals like LinkedIn, Naukri, Glassdoor, and Internshala, discovers HR contacts, enriches data, monitors performance, and optimizes costs — all deployable on Docker locally and AWS in production.

`🔴🔴 For educational purpose only 🔴🔴`      
---

## ⚙️ Development Objectives

### ✅ Stage 1: Local Setup with Docker (Simulation Phase)

| Objective | Tools |
|----------|-------|
| Simulate AWS infrastructure locally | Docker, Docker Compose |
| Run scrapers and database | Selenium, BeautifulSoup, PostgreSQL |
| Track pipeline health | Prometheus, Grafana |
| Schedule jobs | Cron (or Python Scheduler) |
| Store reports | Local filesystem (acts like S3) |

#### Steps:
1. Clone the repository.
2. Spin up services using `docker-compose`.
3. Run scraper containers to fetch job data.
4. Store data into docker PostgreSQL or mongoDB.
5. Visualize metrics in Grafana.
6. Output daily JSON and email templates.

---

### 🚀 Stage 2: Cloud Deployment (Production Phase on AWS)

| Objective | Tools |
|-----------|-------|
| Deploy scalable infra | AWS EC2, RDS, S3, IAM |
| Automate builds and deployments | GitLab CI/CD |
| Monitor production pipeline | Prometheus, Grafana, or CloudWatch |
| Optimize resource cost | Cost Explorer, Prometheus Alerts |

#### Steps:
1. Provision infrastructure using AWS CLI or Terraform.
2. Push Docker images to EC2.
3. Migrate PostgreSQL schema to RDS.
4. Store reports and resumes in S3.
5. Set up Prometheus + Grafana (or use CloudWatch).
6. Use GitLab `.gitlab-ci.yml` for automated deployments and cron schedules.

---

## 📊 Key Components

- **Scrapers**: LinkedIn, Naukri, Internshala, Glassdoor
- **Enrichment pipeline**: HR contact discovery, email pattern matching
- **Database**: PostgreSQL with jobs and contacts schema
- **Monitoring**: Custom metrics (scraping success, job counts, etc.)
- **Frontend**: Angular UI
- **Deployment**: Docker → AWS + GitLab
