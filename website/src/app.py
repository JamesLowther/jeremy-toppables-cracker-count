import json

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    try:
        with open("static/scans/manifest.json", "r") as f:
            manifest = json.loads(f.read())

        version = "v1"
        posts = manifest["posts"]
        updated = manifest["manifest_updated"]
        total = sum([len(x["scans"][version]) for x in posts])

    except FileNotFoundError:
        version=""
        posts = []
        updated = ""
        total = 0

    return render_template("index.html", version=version, posts=posts, updated=updated, total=total)

@app.route("/v2")
def version2():
    try:
        with open("static/scans/manifest.json", "r") as f:
            manifest = json.loads(f.read())

        version = "v2"
        posts = manifest["posts"]
        updated = manifest["manifest_updated"]
        total = sum([len(x["scans"][version]) for x in posts])

    except FileNotFoundError:
        version=""
        posts = []
        updated = ""
        total = 0

    return render_template("index.html", version=version, posts=posts, updated=updated, total=total)
