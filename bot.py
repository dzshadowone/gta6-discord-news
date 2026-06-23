import requests
import os

WEBHOOK = os.environ["WEBHOOK_URL"]

requests.post(WEBHOOK, json={
    "content": "✅ TEST: Discord webhook is working"
})
