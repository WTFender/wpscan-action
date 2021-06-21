import requests
import base64
import json
import sys

RESULTB64 = sys.argv[1]
WEBHOOK = sys.argv[2]
WEBHOOKOPTS = sys.argv[3]

RESULT = base64.b64decode(RESULTB64).decode('utf-8')

if WEBHOOK:
    x = json.loads(RESULT)
    payload = {
        'text': 'testsetsetseting!'
    }

    r = requests.post(WEBHOOK, json=payload)
    print(r.status_code)

else:
    print('No webhook')