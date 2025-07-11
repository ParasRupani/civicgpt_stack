# Dockerfile
FROM apache/airflow:2.8.1-python3.11

USER root
RUN pip install feedparser python-dotenv
USER airflow
