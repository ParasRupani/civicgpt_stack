from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import gzip
import shutil
from pathlib import Path

# Constants
RAW_PATH = "/opt/airflow/data/raw/news"
ARCHIVE_PATH = "/opt/airflow/data/archive/news"
DAYS_OLD = 30  # Threshold for archival

def compress_and_archive_old_json():
    Path(ARCHIVE_PATH).mkdir(parents=True, exist_ok=True)

    for file in os.listdir(RAW_PATH):
        file_path = os.path.join(RAW_PATH, file)
        
        # Only consider .json files
        if file.endswith(".json") and os.path.isfile(file_path):
            # Check file age
            file_age = (datetime.utcnow() - datetime.utcfromtimestamp(os.path.getmtime(file_path))).days
            if file_age > DAYS_OLD:
                archive_file_path = os.path.join(ARCHIVE_PATH, file + ".gz")

                # Compress file
                with open(file_path, 'rb') as f_in:
                    with gzip.open(archive_file_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                os.remove(file_path)  # Delete original file
                print(f"[Archive] Compressed and moved: {file} → {archive_file_path}")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='archive_old_news_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='Compress and archive old JSON news files older than 7 days',
) as dag:

    archive_task = PythonOperator(
        task_id='compress_and_archive_old_files',
        python_callable=compress_and_archive_old_json
    )
