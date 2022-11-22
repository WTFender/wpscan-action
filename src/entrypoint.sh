#!/bin/sh

URL=$1

echo "Updating wpscan";
wpscan --update

echo "Running wpscan on $URL";
python3 wpscan.py $URL
