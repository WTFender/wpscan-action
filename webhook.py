import requests
import os

result = os.getenv('RESULT')
webhook = os.getenv('WEBHOOK')

payload = {
    'text': 'testsetsetseting!'
}

r = requests.post(webhook, json=payload)
print(r.status_code)