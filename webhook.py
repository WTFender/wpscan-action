import requests
import base64
import json
import sys

RESULTB64 = sys.argv[1]
WEBHOOK = sys.argv[2]
WEBHOOKOPTS = sys.argv[3]

RESULT = json.loads(base64.b64decode(RESULTB64).decode('utf-8'))


def scan():
    return {'text': 'Scan completed'}

def abort():
    return {'text': 'Scan aborted'}

def vulns():
    return {'text': 'Vulns found'}



if not WEBHOOK:
    exit('No webhook')   
    
if 'scan_aborted' in RESULT:
    requests.post(WEBHOOK, json=abort())
    exit('Scan aborted')

VULNS = ( len(RESULT['version']['vulnerabilities']) +
        len(RESULT['main_theme']['vulnerabilities']) + 
        sum([len(RESULT['plugins'][p]['vulnerabilities']) for p in RESULT['plugins']]) )

if VULNS:
    requests.post(WEBHOOK, json=vulns())
    exit('Vulns found')

if WEBHOOKOPTS:
    requests.post(WEBHOOK, json=scan())
    exit('Scan completed')
