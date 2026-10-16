import os
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
from dotenv import load_dotenv


def search_news(query, max_results=8):
    """Search news using GNews with Google News RSS fallback."""
    load_dotenv()

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Please enter a topic to search.")

    query = query.strip()[:200]
    max_results = max(1, min(int(max_results), 10))
    api_key = os.getenv("GNEWS_API_KEY", "").strip()

    if api_key:
        try:
            response = requests.get(
                "https://gnews.io/api/v4/search",
                params={
                    "q": query,
                    "lang": "en",
                    "max": max_results,
                    "apikey": api_key,
                },
                timeout=12,
            )

            if response.ok:
                data = response.json()
                articles = []

                for article in data.get("articles", []):
                    source = article.get("source") or {}
                    articles.append({
                        "title": article.get("title", ""),
                        "description": article.get("description", ""),
                        "url": article.get("url", ""),
                        "source": source.get("name", ""),
                        "published_at": article.get("publishedAt", ""),
                    })

                if articles:
                    return {
                        "query": query,
                        "total_results": len(articles),
                        "articles": articles,
                        "provider": "GNews",
                    }

        except (requests.RequestException, ValueError):
            pass

    rss_url = (
        "https://news.google.com/rss/search?q="
        + quote_plus(query)
        + "&hl=en-IN&gl=IN&ceid=IN:en"
    )

    try:
        response = requests.get(
            rss_url,
            timeout=15,
            headers={"User-Agent": "AITruthTrail/1.0"},
        )
        response.raise_for_status()
        root = ET.fromstring(response.content)

    except (requests.RequestException, ET.ParseError) as error:
        raise RuntimeError(
            "News search could not reach Google News RSS. "
            "Check your internet connection and try again."
        ) from error

    articles = []

    for item in root.findall("./channel/item")[:max_results]:
        title = item.findtext("title", default="").strip()
        link = item.findtext("link", default="").strip()
        description = item.findtext("description", default="").strip()
        published_at = item.findtext("pubDate", default="").strip()

        source_node = item.find("source")
        source = (
            (source_node.text or "").strip()
            if source_node is not None
            else ""
        )

        if title and link:
            articles.append({
                "title": title,
                "description": description,
                "url": link,
                "source": source or "Google News RSS",
                "published_at": published_at,
            })

    return {
        "query": query,
        "total_results": len(articles),
        "articles": articles,
        "provider": "Google News RSS",
    }
def analyze_news(text):
    """Provide a basic analysis of news text for AI TruthTrail."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Please provide news text to analyze.")

    return {
        "text": text.strip(),
        "summary": text.strip()[:500],
        "message": "Basic news text analysis completed."
    }