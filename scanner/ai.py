import os
import json
from datetime import datetime
import db

import torch
from detecto import core, utils, visualize
from detecto.utils import reverse_normalize, normalize_transform, _is_iterable
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from torchvision import transforms


SCAN_DIR="scans"

SCORE_THRESHOLD = 0.9

# (version, model)
MODELS = [
    ("v1", "toppables.pth")
]

def check_image(path, version, model, uuid):
    print(f"Scanning {path}")

    image = utils.read_image(path)
    predictions = model.predict(image)
    labels, boxes, scores = predictions

    filtered_boxes = []
    filtered_labels = []

    for i in range(len(scores)):
        if scores[i] >= SCORE_THRESHOLD:
            filtered_labels.append(labels[i])
            filtered_boxes.append(boxes[i])

    if len(filtered_labels) == 0:
        return None

    else:
        scan_dir = f"{SCAN_DIR}/{version}/images/{uuid}"
        if not os.path.exists(scan_dir):
            os.makedirs(scan_dir)

        scan_path = f"{scan_dir}/{os.path.basename(path)}"
        save_image(image, torch.stack(filtered_boxes), filtered_labels, scan_path)

        return scan_path


def save_image(image, boxes, labels, save_path):
    # Modified from https://github.com/alankbi/detecto/blob/master/detecto/visualize.py

    fig, ax = plt.subplots(1)
    # If the image is already a tensor, convert it back to a PILImage
    # and reverse normalize it
    if isinstance(image, torch.Tensor):
        image = reverse_normalize(image)
        image = transforms.ToPILImage()(image)
    ax.imshow(image)

    # Show a single box or multiple if provided
    if boxes.ndim == 1:
        boxes = boxes.view(1, 4)

    if labels is not None and not _is_iterable(labels):
        labels = [labels]

    # Plot each box
    for i in range(boxes.shape[0]):
        box = boxes[i]
        width, height = (box[2] - box[0]).item(), (box[3] - box[1]).item()
        initial_pos = (box[0].item(), box[1].item())
        rect = patches.Rectangle(initial_pos,  width, height, linewidth=1,
                                 edgecolor='r', facecolor='none')
        if labels:
            ax.text(box[0] + 5, box[1] - 5, '{}'.format(labels[i]), color='red')

        ax.add_patch(rect)

    plt.savefig(save_path)

def scan_unscanned_posts():
    "Scanning all unscanned posts"

    scan_dir = f"scans"
    if not os.path.exists(scan_dir):
        os.makedirs(scan_dir)

    con, cur = db.connect()

    cur.execute("SELECT uuid FROM Posts WHERE scanned=0;")
    res = cur.fetchall()

    scan_count = 0

    for row in res:
        uuid = row["uuid"]

        for version, model in MODELS:
            print(f"Scanning version: {version} - model: {model}")
            scan_count = scan_with_version(version, model, uuid)

        cur.execute("UPDATE Posts SET scanned=1 WHERE uuid=?;", (uuid,))
        con.commit()

    con.close()

    return scan_count

def scan_with_version(version, model, uuid):
    con, cur = db.connect()

    model_file = core.Model.load(model, ["toppables"])

    cur.execute("SELECT image_path FROM Images WHERE uuid=? ORDER BY image_order ASC;", (uuid,))
    image_res = cur.fetchall()
    image_paths = [x["image_path"] for x in image_res]

    order = 0
    scan_count = 0

    for path in image_paths:
        scan_path = check_image(path, version, model_file, uuid)

        if scan_path is not None:
            cur.execute("INSERT INTO Scans (scan_path, uuid, image_path, scan_order, version) VALUES (?, ?, ?, ?, ?);", (scan_path, uuid, path, order, version))
            con.commit()

            scan_count += 1
            order += 1

    con.close()

    return scan_count

def write_scan_manifest():
    print("Writing scan manifest")

    con, cur = db.connect()

    cur.execute("SELECT DISTINCT uuid FROM Scans;")
    uuid_res = cur.fetchall()

    cur.execute("SELECT DISTINCT version FROM Scans;")
    version_res = cur.fetchall()

    versions = [ x["version"] for x in version_res ]

    manifest = []

    for row in uuid_res:
        uuid = row["uuid"]

        cur.execute("SELECT * FROM Posts WHERE uuid=?;", (uuid,))
        post_res = cur.fetchone()

        scans = dict()
        for version in versions:
            cur.execute("SELECT * FROM Scans WHERE uuid=? AND version=? ORDER BY scan_order ASC;", (uuid, version))
            scans_res = cur.fetchall()

            scans[version] = [x["scan_path"] for x in scans_res]

        manifest.append(
            {
                "uuid": uuid,
                "title": post_res["title"],
                "url": post_res["url"],
                "updated_at": post_res["updated_at"],
                "scans": scans
            }
        )

    con.close()

    manifest = sorted(manifest, key=lambda x: datetime.fromisoformat(x["updated_at"]), reverse=True)

    manifest = {
        "posts": manifest,
        "manifest_updated": datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
    }

    with open(f"{SCAN_DIR}/manifest.json", "w") as f:
        f.write(json.dumps(manifest))
