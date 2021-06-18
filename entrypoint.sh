#!/bin/sh
WPSCAN=/usr/local/bundle/bin/wpscan

$WPSCAN --update

RESULT=$($WPSCAN --disable-tls-checks --url $1 --api-token $2 -f json)

RESULT_B64=$(echo $RESULT | base64)

echo ::set-output name=result::$RESULT
echo ::set-output name=resultb64::$RESULT_B64
