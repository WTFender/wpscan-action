import requests
import os

result = os.getenv('RESULT')
webhook = os.getenv('WEBHOOK')

payload = {
    'text': 'testsetsetseting!'
}

requests.post(webhook, json=payload)