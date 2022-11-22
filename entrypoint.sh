#!/bin/sh

URL=$1
TOKEN=$2
OPTIONS=$3
WEBHOOK=$4
WEBHOOKEVENT=$5

ARGS="-f json --url ${URL}"
[  -n "$2" ] && ARGS="${ARGS} --api-token=${TOKEN}"
[  -n "$3" ] && ARGS="${ARGS} ${OPTIONS}"

WPSCAN=/usr/local/bundle/bin/wpscan

$WPSCAN --update

#RESULT=$(cat /example.json)
RESULT=$($WPSCAN $ARGS -o result.json; cat result.json)
RESULT_B64=$(echo $RESULT | base64)

cat result.json | grep -i limit
echo "result<<EOF" >> $GITHUB_OUTPUT
echo "$RESULT" >> $GITHUB_OUTPUT
echo "EOF" >> $GITHUB_OUTPUT


echo "resultb64<<EOF" >> $GITHUB_OUTPUT
echo "$RESULT_B64" >> $GITHUB_OUTPUT
echo "EOF" >> $GITHUB_OUTPUT


python3 /webhook.py "${RESULT_B64}" "${WEBHOOK}" "${WEBHOOKEVENT}"
