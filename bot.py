import os
import re
import requests
import feedparser
from bs4 import BeautifulSoup

WEBHOOK = os.environ["WEBHOOK_URL"]

FEEDS = [
    "https://rockstarintel.com/feed/",
    "https://www.gtabase.com/feed/",
    "https://www.thegta6updates.com/feed/"
]

POSTED_FILE = "posted_urls.txt"

# Load already posted URLs
if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE, "r", encoding="utf-8") as f:
        posted_urls = set(line.strip() for line in f)
else:
    posted_urls = set()

new_urls = []

for feed_url in FEEDS:
    try:
        feed = feedparser.parse(feed_url)

        for article in feed.entries:

            title = article.get("title", "")
            url = article.get("link", "")

            if not url:
                continue

            title_lower = title.lower()

            allowed = (
                "gta 6" in title_lower or
                "gta vi" in title_lower or
                "grand theft auto vi" in title_lower
            )

            blocked = (
                "gta 5" in title_lower or
                "gta v" in title_lower or
                "red dead" in title_lower
            )

            if not allowed or blocked:
                continue

            if url in posted_urls:
                continue

            summary = re.sub("<.*?>", "", article.get("summary", ""))[:3000]

            image = None

            try:
                response = requests.get(
                    url,
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=10
                )

                soup = BeautifulSoup(response.text, "lxml")

                og = soup.find("meta", property="og:image")
                if og and og.get("content"):
                    image = og["content"]

                if not image:
                    twitter = soup.find("meta", attrs={"name": "twitter:image"})
                    if twitter and twitter.get("content"):
                        image = twitter["content"]

            except Exception as e:
                print("Image error:", str(e))

            embed = {
                "title": title,
                "description": summary,
                "url": url,
                "color": 3066993
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

            print("Posted:", title)

            posted_urls.add(url)
            new_urls.append(url)

    except Exception as e:
        print("Feed error:", feed_url, str(e))

# Save posted URLs
if new_urls:
    with open(POSTED_FILE, "a", encoding="utf-8") as f:
        for url in new_urls:
            f.write(url + "\n")

print("Done")