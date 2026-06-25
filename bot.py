import os
import requests

WEBHOOK = os.environ["WEBHOOK_URL"]

# Example RSS feed
rss = requests.get(
    "https://www.rockstargames.com/newswire/rss"
).text

payload = {
    "content": "📰 New Rockstar News Available:\nhttps://www.rockstargames.com/newswire"
}

requests.post(WEBHOOK, json=payload)