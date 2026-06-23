import os
import requests

print("STARTED")

webhook = os.environ.get("WEBHOOK_URL")
print("WEBHOOK EXISTS:", bool(webhook))

payload = {
    "content": "🚨 TEST MESSAGE FROM GITHUB ACTIONS"
}

try:
    r = requests.post(webhook, json=payload)

    print("STATUS CODE:", r.status_code)
    print("RESPONSE TEXT:", r.text)

except Exception as e:
    print("ERROR:", str(e))
