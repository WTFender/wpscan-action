import requests
import sys
import os

RESULT = os.getenv('RESULT')
WEBHOOK = sys.argv[2]

if WEBHOOK:
    payload = {
        'text': 'testsetsetseting!'
    }

    r = requests.post(WEBHOOK, json=payload)
    print(r.status_code)

else:
    print('No webhook')