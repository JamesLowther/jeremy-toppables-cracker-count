import requests
import json
from bs4 import BeautifulSoup

def get_posts():
    endpoint = "https://blog.jstuart.ca"
    key = "e10981406c22cfddf07d7beb70"

    posts = []
    page = 1
    while True:
        r = requests.get(f"{endpoint}/ghost/api/content/posts", params={"key": key, "fields": "uuid,html", "page": page})
        j = r.json()

        posts += j["posts"]
        page += 1

        if j["meta"]["pagination"]["next"] is None:
            break

    return posts

def parse_post(post):
    parsed_html = BeautifulSoup(post["html"])

    images = parsed_html.find_all("img")

    for image in images:
        path = image.get("src")
        print(path)

def main():
    posts = get_posts()
    parse_post(posts[0])


if __name__ == "__main__":
    main()
