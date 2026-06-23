import requests
import os

WEBHOOK = os.environ["WEBHOOK_URL"]

print("Sending test message...")

r = requests.post(WEBHOOK, json={
    "content": "✅ TEST MESSAGE: webhook is working"
})

print("Status code:", r.status_code)
print("Response:", r.text)
