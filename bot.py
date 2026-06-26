import os
import re
import requests
import feedparser

WEBHOOK = os.environ["WEBHOOK_URL"]

FEEDS = [
    "https://rockstarintel.com/feed/",
    "https://www.gtabase.com/feed/",
    "https://www.thegta6updates.com/feed/"
]

POSTED_FILE = "posted_urls.txt"

# Charger les URLs déjà envoyées
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

            summary = article.get("summary", "")[:3000]

            # -----------------------------
            # Find an image
            # -----------------------------
            image = None

            # media_content
            if hasattr(article, "media_content"):
                try:
                    image = article.media_content[0]["url"]
                except:
                    pass

            # media_thumbnail
            if not image and hasattr(article, "media_thumbnail"):
                try:
                    image = article.media_thumbnail[0]["url"]
                except:
                    pass

            # enclosure images
            if not image and hasattr(article, "links"):
                for link in article.links:
                    if link.get("type", "").startswith("image"):
                        image = link.get("href")
                        break

            # Image inside summary HTML
            if not image:
                match = re.search(r'<img[^>]+src="([^"]+)"', article.get("summary", ""))
                if match:
                    image = match.group(1)

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

# Sauvegarder les nouvelles URLs
if new_urls:
    with open(POSTED_FILE, "a", encoding="utf-8") as f:
        for url in new_urls:
            f.write(url + "\n")

print("Done")