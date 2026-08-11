import os
import re
import requests
import feedparser
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
from datetime import datetime, timedelta, timezone
import time

WEBHOOK = os.environ["WEBHOOK_URL"]

FEEDS = [
    "https://rockstarintel.com/feed/",
    "https://www.gtabase.com/feed/",
    "https://www.thegta6updates.com/feed/"
]

POSTED_FILE = "posted_urls.txt"

def normalize_url(url):
    """Strip query parameters and fragments to prevent parameter-based duplicates."""
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

# Load already posted URLs and IDs
if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE, "r", encoding="utf-8") as f:
        posted_urls = set(line.strip() for line in f if line.strip())
else:
    posted_urls = set()

new_urls = []

# Exclude articles older than 2 days
MAX_AGE = timedelta(days=2)
now = datetime.now(timezone.utc)

for feed_url in FEEDS:
    try:
        feed = feedparser.parse(feed_url)

        for article in feed.entries:
            title = article.get("title", "")
            raw_url = article.get("link", "")
            article_id = article.get("id", article.get("guid", raw_url))

            if not raw_url:
                continue

            # Check publication date if available
            published_parsed = article.get("published_parsed") or article.get("updated_parsed")
            if published_parsed:
                pub_date = datetime.fromtimestamp(time.mktime(published_parsed), tz=timezone.utc)
                if now - pub_date > MAX_AGE:
                    continue  # Skip old articles

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

            clean_url = normalize_url(raw_url)

            # Fast-check against cache before doing HTTP requests
            if clean_url in posted_urls or article_id in posted_urls:
                continue

            summary = re.sub("<.*?>", "", article.get("summary", ""))[:3000]
            image = None
            final_target_url = clean_url

            try:
                response = requests.get(
                    raw_url,
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=10
                )

                soup = BeautifulSoup(response.text, "lxml")

                # Resolve canonical URL to catch redirects
                canonical = soup.find("link", rel="canonical")
                if canonical and canonical.get("href"):
                    final_target_url = normalize_url(canonical["href"])

                if final_target_url in posted_urls:
                    continue

                # Image extraction
                og = soup.find("meta", property="og:image")
                if og and og.get("content"):
                    image = og["content"]

                if not image:
                    twitter = soup.find("meta", attrs={"name": "twitter:image"})
                    if twitter and twitter.get("content"):
                        image = twitter["content"]

            except Exception as e:
                print("HTTP error for", raw_url, ":", str(e))

            embed = {
                "title": title,
                "description": summary,
                "url": raw_url,
                "color": 3066993
            }

            if image:
                embed["image"] = {"url": image}

            requests.post(
                WEBHOOK,
                json={
                    "content": "@everyone",
                    "embeds": [embed]
                }
            )

            print("Posted:", title)

            # Store clean URLs and RSS item IDs
            posted_urls.add(clean_url)
            posted_urls.add(final_target_url)
            posted_urls.add(article_id)

            new_urls.extend([clean_url, final_target_url, article_id])

    except Exception as e:
        print("Feed error:", feed_url, str(e))

# Save posted items
if new_urls:
    with open(POSTED_FILE, "a", encoding="utf-8") as f:
        for item in set(new_urls):
            f.write(item + "\n")

print("Done")
