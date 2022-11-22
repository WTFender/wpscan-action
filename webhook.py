import requests
import base64
import json
import sys


RESULTB64 = sys.argv[1]
WEBHOOK = sys.argv[2]
WEBHOOKEVENTS = sys.argv[3].split(',')
RESULT = json.loads(base64.b64decode(RESULTB64).decode('utf-8'))


def scan():
    print('Scan completed')
    return {
        'username': 'WPScan',
        'text': 'Scan completed for %s' % RESULT['target_url'],
        'color': 'success'
    }


def abort():
    return {
        'username': 'WPScan',
        'text': 'Scan aborted for %s' % RESULT['target_url'],
        'color': 'danger'
    }


def vulns():
    print('Vulns found')
    attachments = []

    def parseVuln(v):
        vuln = {
            "color": "danger",
            "fallback": v['title'],
            "title": v['title'],
            "fields": []
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
        return vuln

    for v in RESULT['version']['vulnerabilities']:
        vuln = parseVuln(v)
        vuln['fields'].append({
                        'title': 'Version',
                        'value': f"{RESULT['version']['number']} ({RESULT['version']['confidence']}%)",
                        'short': True
                    })
        attachments.append(vuln)
    
    for v in RESULT['main_theme']['vulnerabilities']:
        vuln = parseVuln(v)
        vuln['fields'].append({
                        'title': 'Version',
                        'value': f"{RESULT['main_theme']['version']['number']} ({RESULT['main_theme']['version']['confidence']}%)",
                        'short': True
                    })
        attachments.append(vuln)
    
    for p in RESULT['plugins']:
        for v in RESULT['plugins'][p]['vulnerabilities']:
            vuln = parseVuln(v)
            # Edge case where the WPScan is not able to identify the plugin version
            if not (RESULT['plugins'][p]['version'] is None):
                version = f"{RESULT['plugins'][p]['version']['number']} ({RESULT['plugins'][p]['version']['confidence']}%)"
            else:
                version = "Unknown"
            vuln['fields'].append({
                        'title': 'Version',
                        'value': f"{version}",
                        'short': True
                    })
            attachments.append(vuln)

    return {
        'username': 'WPScan',
        'text': 'Vulnerabilities found for %s' % RESULT['target_url'],
        'attachments': attachments
    }

if __name__ == '__main__':

    event = None

    # Aborted scan
    if 'scan_aborted' in RESULT:
        event = 'aborted'
        payload = abort()
    
    # Completed scan
    else:
        event = 'completed'
        payload = scan()

        VULNS = ( len(RESULT['version']['vulnerabilities']) +
                len(RESULT['main_theme']['vulnerabilities']) + 
                sum([len(RESULT['plugins'][p]['vulnerabilities']) for p in RESULT['plugins']]) )

        # Vulns found
        if VULNS:
            event = 'vulns'
            payload = vulns()

    if WEBHOOK and event in WEBHOOKEVENTS:
        # Send webhook
        r = requests.post(WEBHOOK, json=payload)
        print(f'Webhook: %s' % r.status_code)
