import json

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    try:
        with open("static/scans/manifest.json", "r") as f:
            manifest = json.loads(f.read())

        posts = manifest["posts"]
        updated = manifest["manifest_updated"]
        total = sum([len(x["scans"]) for x in posts])

    except FileNotFoundError:
        posts = []
        updated = ""
        total = 0

    return render_template("index.html", posts=posts, updated=updated, total=total)
