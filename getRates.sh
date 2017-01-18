#!/bin/sh
echo "Current date is `date`"

current_time=$(date +"%Y_%m_%d_%H")
python3 ~/Downloads/scrape.py $current_time.csv
