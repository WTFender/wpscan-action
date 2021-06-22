import requests
import base64
import json
import sys

RESULTB64 = sys.argv[1]
WEBHOOK = sys.argv[2]
WEBHOOKOPTS = sys.argv[3]

RESULT = json.loads(base64.b64decode(RESULTB64).decode('utf-8'))


def scan():
    print('Scan completed')
    return {'text': 'Scan completed'}
    
def abort():
    print('Scan aborted')
    return {'text': 'Scan aborted'}

def vulns(n):
    print('Vulns found')
    return {'text': '%s vulns found' % n}
    

if 'scan_aborted' in RESULT:
    payload = abort()

VULNS = ( len(RESULT['version']['vulnerabilities']) +
        len(RESULT['main_theme']['vulnerabilities']) + 
        sum([len(RESULT['plugins'][p]['vulnerabilities']) for p in RESULT['plugins']]) )

if VULNS:
    payload = vulns(VULNS)

if WEBHOOK:
    r = requests.post(WEBHOOK, json=payload)
    print(f'Webhook: %s' % r.status_code)
    