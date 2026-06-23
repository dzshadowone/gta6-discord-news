import os

print("START")

print("ENV:", dict(os.environ))

print("WEBHOOK:", os.environ.get("WEBHOOK_URL"))
