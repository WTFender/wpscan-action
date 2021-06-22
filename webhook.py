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
    return {'text': 'Scan completed', 'color': 'success'}
    
def abort():
    print('Scan aborted')
    return {'text': 'Scan aborted', 'color': 'warning'}

def vulns(n):
    print('Vulns found')
    attachments = []

    #for v in RESULT['version']['vulnerabilities']:
    #    pass
    #
    #for v in RESULT['main_theme']['vulnerabilities']:
    #    pass
    
    for p in RESULT['plugins']:
        for v in RESULT['plugins'][p]['vulnerabilities']:
            version = f"{RESULT['plugins'][p]['version']['number']} ({RESULT['plugins'][p]['version']['confidence']}%)"
            vuln = {
                "color": "danger",
                "fallback": v['title'],
                "title": v['title'],
                "fields": [
                    {
                        'title': 'Version',
                        'value': version,
                        'short': True
                    }
                ]
            }
            
            if 'url' in v['references']:
                vuln['title_link'] = v['references']['url'][0]

            if 'cve' in v['references']:
                cve = 'CVE-'+v['references']['cve'][0]
                vuln['author_name'] = cve
                vuln['author_link'] = 'https://cve.mitre.org/cgi-bin/cvename.cgi?name='+cve

            if 'fixed_in' in v:
                vuln['fields'].append(
                    {
                        'title': 'Fixed Version',
                        'value': v['fixed_in'],
                        'short': True
                    }
                )
            attachments.append(vuln)

    return {
        'username': 'WPScan',
        'text': 'Vulnerabilities found',
        'attachments': attachments
    }
    

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
