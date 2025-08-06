#!/bin/bash

echo "Starting PostgreSQL initialization..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL

\connect app_db;

-- Create schema owned by app_user
CREATE SCHEMA IF NOT EXISTS job AUTHORIZATION ${APP_USER};

CREATE TABLE IF NOT EXISTS job.job_details (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    company VARCHAR(255),
    location VARCHAR(100),
    start_date VARCHAR(100),
    duration VARCHAR(100),
    stipend VARCHAR(100),
    apply_by VARCHAR(100),
    responsibilities TEXT,
    skills_required TEXT,
    other_requirements TEXT,
    perks TEXT,
    openings VARCHAR(50),
    company_description TEXT,
    posted_date VARCHAR(100),
    company_url VARCHAR(255),
    url VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_job_details_url ON job.job_details(url);

-- Grant privileges to app_user
GRANT USAGE ON SCHEMA job TO ${APP_USER};
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA job TO ${APP_USER};

-- Permissions for sequences (primary keys)
GRANT USAGE, SELECT ON SEQUENCE job.job_details_id_seq TO ${APP_USER};

EOSQL
