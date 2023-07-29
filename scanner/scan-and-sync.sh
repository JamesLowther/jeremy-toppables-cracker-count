#!/bin/bash

cd $(dirname $0)

source ./.venv/bin/activate
python3 main.py

echo "Syncing with rsync"
rsync -a --delete ./scans toppables@vps.jameslowther.com:~/jeremy-toppables-cracker-count/website
