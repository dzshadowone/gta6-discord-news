import os
import requests
import feedparser
from deep_translator import GoogleTranslator

WEBHOOK = os.environ["WEBHOOK_URL"]

FEEDS = [
    "https://rockstarintel.com/feed/",
    "https://www.gtabase.com/feed/",
    "https://gta6updates.com/feed/"
]

articles = []

for feed_url in FEEDS:
    try:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            articles.append(entry)

    except Exception as e:
        print("Feed error:", e)

if not articles:
    print("No articles found")
    exit()

article = articles[0]

title = article.get("title", "No title")
url = article.get("link", "")
summary = article.get("summary", "")

try:
    title_ar = GoogleTranslator(source="auto", target="ar").translate(title)
except:
    title_ar = title

try:
    summary_ar = GoogleTranslator(source="auto", target="ar").translate(summary[:1500])
except:
    summary_ar = summary[:1500]

image = None

if "media_content" in article:
    try:
        image = article.media_content[0]["url"]
    except:
        pass

embed = {
    "title": title_ar,
    "description": summary_ar[:3000],
    "url": url
}

if image:
    embed["image"] = {
        "url": image
    }

requests.post(
    WEBHOOK,
    json={
        "content": "@everyone",
        "embeds": [embed]
    }
)

print("News sent")