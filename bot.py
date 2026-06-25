import os
import requests
import feedparser

WEBHOOK = os.environ["WEBHOOK_URL"]

# GTA-focused source
FEED_URL = "https://rockstarintel.com/feed/"

feed = feedparser.parse(FEED_URL)

if len(feed.entries) == 0:
    print("No articles found")
    exit()

article = feed.entries[0]

title = article.title
url = article.link
summary = article.summary[:1000]

image = None

if "media_content" in article:
    image = article.media_content[0]["url"]

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