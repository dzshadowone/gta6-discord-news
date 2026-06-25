embed = {
    "title": article_title,
    "description": article_summary[:1000],
    "url": article_url,
    "image": {
        "url": article_image
    },
    "footer": {
        "text": "GTA 6 News Bot"
    }
}

requests.post(
    WEBHOOK,
    json={"embeds": [embed]}
)