import requests
import os

print("BOT STARTED")

webhook = os.environ.get("WEBHOOK_URL")

print("WEBHOOK:", webhook)

if not webhook:
    print("ERROR: WEBHOOK_URL is missing")
    exit()

print("Sending Discord message...")

response = requests.post(webhook, json={
    "content": "✅ TEST: bot is working correctly"
})

print("STATUS:", response.status_code)
print("RESPONSE:", response.text)
