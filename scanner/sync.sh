#!/bin/bash

cd $(dirname $0)

rsync -a --delete ./scans james@vps.jameslowther.com:~/jeremy-toppables-cracker-count/website
