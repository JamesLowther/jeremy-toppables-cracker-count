import json

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    with open("static/scans/manifest.json", "r") as f:
        manifest = json.loads(f.read())

    total = sum([len(x["scans"]) for x in manifest])

    return render_template("index.html", manifest=manifest, total=total)
