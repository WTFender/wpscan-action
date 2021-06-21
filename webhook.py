import requests
import os

RESULT = os.getenv('RESULT')
WEBHOOK = os.getenv('WEBHOOK')

if WEBHOOK:
    payload = {
        'text': 'testsetsetseting!'
    }

    r = requests.post(WEBHOOK, json=payload)
    print(r.status_code)

else:
    print('No webhook')