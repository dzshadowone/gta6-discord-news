import os
import requests
import feedparser

WEBHOOK = os.environ["WEBHOOK_URL"]

FEEDS = [
    "https://rockstarintel.com/feed/",
    "https://www.gtabase.com/feed/",
    "https://gta6updates.com/feed/"
]

articles = []

for feed_url in FEEDS:
    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        articles.append(entry)

if not articles:
    print("No articles found")
    exit()

# Most recent article
article = articles[0]

title = article.get("title", "No title")
url = article.get("link", "")
summary = article.get("summary", "")[:1000]

image = None

if "media_content" in article:
    image = article.media_content[0].get("url")

embed = {
    "title": title,
    "description": summary,
    "url": url
}

if image:
    embed["image"] = {
        "url": image
    }

requests.post(
    WEBHOOK,
    json={"embeds": [embed]}
)

print("News sent")