import feedparser
import urllib.request
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from utils.news_schema import NewsArticle
from urllib.error import URLError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import hashlib

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

def normalize_field(entry, key):
    value = entry.get(key, "")
    if isinstance(value, list):
        value = value[0] if value else ""
    return str(value).strip() if value else ""

def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text().strip()

def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ["http", "https"] and bool(parsed.netloc)
    except Exception:
        return False

def generate_article_id(link: str) -> str:
    return hashlib.md5(link.encode()).hexdigest()

def fetch_rss():
    FEED_URLS = [
        "http://rss.cbc.ca/lineup/canada-kitchenerwaterloo.xml",
        "http://rss.cbc.ca/lineup/canada-toronto.xml",
        "https://www.cbc.ca/webfeed/rss/rss-canada"
    ]

    all_articles = []
    seen_ids = set()

    save_path = "/opt/airflow/data/raw/news"
    os.makedirs(save_path, exist_ok=True)
    filename = f"{save_path}/{datetime.now().strftime('%Y-%m-%d')}.json"

    # Load existing articles (if file exists)
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                existing_articles = json.load(f)
                seen_ids = {a["id"] for a in existing_articles if "id" in a}
                all_articles.extend(existing_articles)
        except Exception as e:
            print(f"[Warning] Failed to read existing file: {e}")

    for FEED_URL in FEED_URLS:
        print(f"[Info] Fetching feed: {FEED_URL}")
        try:
            request = urllib.request.Request(
                FEED_URL,
                headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Accept': 'application/rss+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Referer': 'https://www.cbc.ca'
                }
            )
            with urllib.request.urlopen(request, timeout=10) as response:
                raw_data = response.read()

            feed = feedparser.parse(raw_data)

            for entry in feed.entries:
                try:
                    title = normalize_field(entry, "title")
                    summary_html = normalize_field(entry, "summary")
                    link_str = normalize_field(entry, "link")
                    published = normalize_field(entry, "published")
                    article_id = generate_article_id(link_str)

                    if not is_valid_url(link_str):
                        raise ValueError(f"Invalid link: {link_str}")
                    
                    if article_id in seen_ids:
                        continue

                    article = NewsArticle(
                        title=title,
                        summary=clean_html(summary_html),
                        link=link_str,
                        published=published,
                        source=FEED_URL,
                        id=article_id
                    )

                    article_dict = article.model_dump(mode="json")
                    article_dict["id"] = article_id

                    all_articles.append(article_dict)
                    seen_ids.add(article_id)

                except Exception as e:
                    print(f"[⚠️ Skipping] {title[:60]} | link={link_str} | error={e}")

        except URLError as e:
            print(f"[Feed Error] Unable to fetch feed: {FEED_URL} — {e}")
        except Exception as e:
            print(f"[Feed Error] General error fetching/parsing feed: {FEED_URL} — {e}")

    # Save to file
    with open(filename, "w") as f:
        json.dump(all_articles, f, indent=2)

    print(f"[Saved] {len(all_articles)} total articles written to {filename}")