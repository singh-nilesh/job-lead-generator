#!/bin/bash

sudo rm -r ./infra/mongo/data
sudo rm -r ./infra/postgres/data

sudo mkdir -p ./artifacts/logs
sudo chmod -R 777 ./artifacts  # rwx for all users
sudo chmod +x ./infra/airflow/user_init.sh

