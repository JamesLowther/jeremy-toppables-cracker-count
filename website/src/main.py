import json

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    try:
        with open("static/scans/manifest.json", "r") as f:
            manifest = json.loads(f.read())

        total = sum([len(x["scans"]) for x in manifest])

    except FileNotFoundError:
        manifest = []
        total = 0

    return render_template("index.html", manifest=manifest, total=total)
