import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

def send_webhook(new_posts, new_images, new_scans):
    url = os.environ["WEBHOOK_URL"]

    description = f"New posts: **{new_posts}**\n"
    description += f"New images: **{new_images}**\n"
    description += f"New scans: **{new_scans}**"

    data = {
        "content" : "",
    }

    color =0x06a73d

    data["embeds"] = [
        {
            "title" : "Jeremy's Toppables Count",
            "description" : description,
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                 "text": "Toppables"
            }
        }
    ]

    requests.post(url, json=data)


def send_error(e):
    url = os.environ["WEBHOOK_URL"]

    description = f"Exception: {e}"

    data = {
        "content" : "",
    }

    color =0x06a73d

    data["embeds"] = [
        {
            "title" : "Jeremy's Toppables Count",
            "description" : description,
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                 "text": "Toppables"
            }
        }
    ]

    requests.post(url, json=data)

