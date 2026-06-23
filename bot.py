import os
import requests

print("START")

webhook = os.environ.get("WEBHOOK_URL")
print("WEBHOOK EXISTS:", webhook is not None)

r = requests.post(webhook, json={
    "content": "🚨 FINAL TEST: Discord webhook is working"
})

print("STATUS CODE:", r.status_code)
print("RESPONSE:", r.text)
