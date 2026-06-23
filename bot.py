import requests
import feedparser
import os

WEBHOOK = os.environ["WEBHOOK_URL"]

FEEDS = [
    "https://www.gamespot.com/feeds/mashup/",
    "https://www.ign.com/rss/articles",
]

def send_discord(title, link):
    data = {
        "content": f"🚨 GTA 6 Update:\n**{title}**\n{link}"
    }
    requests.post(WEBHOOK, json=data)

for url in FEEDS:
    feed = feedparser.parse(url)

    for entry in feed.entries[:3]:
        if "gta" in entry.title.lower() or "rockstar" in entry.title.lower():
            send_discord(entry.title, entry.link)
