#!/bin/bash
set -e

# Create app_user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER ${APP_USER} WITH PASSWORD '${APP_PASSWORD}';
EOSQL

# Create app_db with app_user as owner
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE app_db OWNER ${APP_USER};
EOSQL

# Create airflow user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER ${AF_USER} WITH PASSWORD '${AF_PASSWORD}';
EOSQL

# Create airflow_db with airflow user as owner
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE airflow_db OWNER ${AF_USER};
EOSQL
