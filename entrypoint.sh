#!/bin/sh -l

/usr/local/bundle/wpscan --update

curl $1

/usr/local/bundle/wpscan --disable-tls-checks --url $1 --api-token $2 -f json -o result.json

RESULT=$(cat result.json | base64)

echo ::set-output name=result::$RESULT

