#!/bin/bash
docker-compose run airflow-webserver airflow db init

docker-compose run airflow-webserver airflow users create \
  --username admin \
  --password admin \
  --firstname Civic \
  --lastname GPT \
  --role Admin \
  --email civic@gpt.com
