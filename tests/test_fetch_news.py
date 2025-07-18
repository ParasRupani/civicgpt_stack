import pytest
from unittest.mock import patch, MagicMock
from airflow.utils.fetch_news import fetch_rss

@patch("airflow.utils.fetch_news.feedparser.parse")
@patch("airflow.utils.fetch_news.open")
@patch("airflow.utils.fetch_news.os.makedirs")
def test_fetch_rss(mock_makedirs, mock_open, mock_parse):
    # Sample fake feed entry
    mock_parse.return_value.entries = [{
        "title": "Sample News",
        "link": "https://www.example.com/article",
        "published": "2025-07-10T12:00:00",
        "summary": "Example summary",
    }]

    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file

    # Run the function
    fetch_rss()

    # Assertions
    mock_parse.assert_called_once()
    mock_makedirs.assert_called_once()
    mock_open.assert_called_once()

    written_data = mock_file.write.call_args[0][0]
    assert "Sample News" in written_data
