from dotenv import load_dotenv
import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import logging

# Add project root to path
DAGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(DAGS_DIR, ".."))
sys.path.insert(0, ROOT_DIR)

# Import fetch function
from utils.fetch_news import fetch_rss

# Load environment variables
load_dotenv(dotenv_path=os.path.join(ROOT_DIR, '.env'))

# Task failure alert
def task_failure_alert(context):
    dag_id = context.get('dag').dag_id
    task_id = context.get('task_instance').task_id
    exec_date = context.get('execution_date')
    log_url = context.get('task_instance').log_url

    logging.error(
        f"""
        Task Failed:
        DAG ID: {dag_id}
        Task ID: {task_id}
        Execution Time: {exec_date}
        Log URL: {log_url}
        """
    )

default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": task_failure_alert,
}

with DAG(
    dag_id="rss_ingest_dag",
    description="Fetch civic news from CBC RSS feeds, validate and store as JSON",
    schedule_interval="@daily",
    start_date=datetime(2025, 7, 10),
    catchup=False,
    default_args=default_args,
    tags=["rss", "news", "ingestion"],
) as dag:

    fetch_news_task = PythonOperator(
        task_id="fetch_rss_news",
        python_callable=fetch_rss
    )

    transform_news = BashOperator(
        task_id='transform_news',
        bash_command='spark-submit /opt/airflow/app/etl/spark_transform.py',
        dag=dag,
    )
    
    fetch_news_task >> transform_news
    