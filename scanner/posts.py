import os
import db
import requests

from bs4 import BeautifulSoup

ENDPOINT = "https://blog.jstuart.ca"
KEY = "e10981406c22cfddf07d7beb70"

SIZE = "w600"

def get_posts():
    posts = []
    page = 1
    while True:
        print(f"Getting post from api - page {page}")
        r = requests.get(f"{ENDPOINT}/ghost/api/content/posts", params={"key": KEY, "fields": "uuid,title,updated_at,url,html", "page": page})

        if r.status_code != 200:
            raise Exception(f"Error hitting blog api")

        j = r.json()

        posts += j["posts"]
        page += 1

        if j["meta"]["pagination"]["next"] is None:
            break

    return posts

def filter_posts(all_posts, limit=None):
    con, cur = db.connect()
    cur.execute("SELECT uuid FROM POSTS;")
    res = cur.fetchall()
    con.close()

    existing_uuids = [ x["uuid"] for x in res ]

    count = 0
    new_posts = []
    for post in all_posts:
        if post["uuid"] not in existing_uuids:
            if limit is not None and count >= limit:
                break

            new_posts.append(post)
            count += 1

    return new_posts

def download_post_images(post):
    print(f"Downloading images for {post['uuid']}")

    con, cur = db.connect()

    image_dir = f"images/{post['uuid']}"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    parsed_html = BeautifulSoup(post["html"])
    images = parsed_html.find_all("img")

    order = 0
    image_count = 0
    for image in images:
        image_url = image.get("src")
        i = image_url.find("images/")
        image_url = image_url[:i + 7] + f"size/{SIZE}/" + image_url[i + 7:]

        file_name = os.path.basename(image_url)

        if file_name.split(".")[-1] not in {"jpg", "jpeg", "png"}:
            continue

        download_path = f"{image_dir}/{file_name}"

        print(f"Downloading {image_url}")
        r = requests.get(image_url)

        if r.status_code != 200:
            raise Exception(f"Error downloading image at path {image_url}")

        with open(download_path, "wb") as f:
            f.write(r.content)

        cur.execute("INSERT INTO Images VALUES (?, ?, ?);", (download_path, post["uuid"], order))

        image_count += 1
        order += 1

    print()

    cur.execute("INSERT INTO Posts VALUES (?, ?, ?, ?, ?, ?);", (post["uuid"], post["title"], post["updated_at"], post["url"], post["html"], 0))

    con.commit()
    con.close()

    return image_count
