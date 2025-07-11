from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import feedparser
import urllib.request
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


def fetch_rss():
    FEED_URLS = [
    "http://rss.cbc.ca/lineup/canada-kitchenerwaterloo.xml",
    "http://rss.cbc.ca/lineup/canada-toronto.xml",
    "https://www.cbc.ca/webfeed/rss/rss-canada"
    ]

    articles = []

    for FEED_URL in FEED_URLS:
        request = urllib.request.Request(
            FEED_URL,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/rss+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': 'https://www.cbc.ca'
            }
        )

        with urllib.request.urlopen(request) as response:
            raw_data = response.read()
            feed = feedparser.parse(raw_data)

        for entry in feed.entries:
            articles.append({
                "title": entry.title,
                "summary": entry.summary,
                "link": entry.link,
                "published": entry.published,
                "source": FEED_URL  # Optional: tag the source
            })

    # Save to mounted Docker volume
    save_path = "/opt/airflow/data/raw/news"
    os.makedirs(save_path, exist_ok=True)
    filename = f"{save_path}/{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(filename, "w") as f:
        json.dump(articles, f, indent=2)


with DAG(
    dag_id="rss_ingest_dag",
    description="Fetch civic news from CBC RSS",
    schedule_interval="@daily",
    start_date=datetime(2025, 7, 10),
    catchup=False,
    tags=["rss", "news"],
) as dag:

    fetch_news = PythonOperator(
        task_id="fetch_rss_news",
        python_callable=fetch_rss
    )
    