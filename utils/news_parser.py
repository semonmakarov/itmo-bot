import feedparser
import requests
from bs4 import BeautifulSoup


def get_latest_news():
    try:
        # RSS парсинг
        feed = feedparser.parse("https://news.itmo.ru/")
        news = []

        for entry in feed.entries[:3]:
            news.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published
            })

        return news

    except Exception as e:
        return []