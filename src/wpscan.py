import os
import sys
import requests
import logging
import json
import subprocess


class Vulnerability():
    """Data class for representing a vulnerability"""

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.type = kwargs.get('type')
        self.title_link = ''
        self.author_name = ''
        self.author_link = ''
        self.fields = []

    def set_title_link(self, link):
        self.title_link = link

    def set_author_name(self, author_name):
        self.author_name = author_name

    def set_author_link(self, author_link):
        self.author_link = author_link

    def add_field(self, title, value):
        self.fields.append({
            'title': title,
            'value': value,
            'short': True
        })

    def generate_slack_attachment(self):
        """Returns a slack attachment for the vulnerability"""
        return {
            'title': self.title,
            'fallback': self.title,
            'color': 'danger',
            'fields': self.fields,
            'title_link': self.title_link,
            'author_link': self.author_link,
            'author_name': self.author_name,
        }


class SlackNotifier():
    """Class for notifying slack about vulnerabilities"""

    def _get_slack_webhook_url(self):
        webhook = os.environ.get('SLACK_WEBHOOK_URL', None)
        if webhook is None:
            raise Exception('SLACK_WEBHOOK_URL environment variable must be provided.')
        return webhook

    def _post_to_slack(self):
        """Posts the payload to slack"""
        response = requests.post(self._get_slack_webhook_url(), json=self.payload)
        if not response.status_code == 200:
            logging.error("Slack was not successfully notified")

    def post_vulnerabilities(self, site_url, vulnerabilities):
        """Post a message to slack indicating a new vulnerability was found."""
        self.payload = {
            'username': 'WPScan',
            'text': f'Vulnerabilities found for {site_url}',
            'attachments': [v.generate_slack_attachment() for v in vulnerabilities],
        }
        self._post_to_slack()


class FiixWordPressScanner():
    """Class for wrapping the wpscan binary and sending results to slack"""

    def __init__(self):
        self._set_defaults()
        self.notifier = SlackNotifier()

    def _set_defaults(self):
        """Sets defaults for the application"""
        self.wp_scan_binary_path = "wpscan"
        self.vulnerabilities = []
        self.result_file_name = 'result.json'

    def _get_api_token(self):
        """Returns the wp scan API token"""
        token = os.environ.get('WP_SCAN_API_TOKEN')
        if not token:
            raise Exception('WP_SCAN_API_TOKEN environment variable not provided')
        return token

    def post_vulnerabilities_to_slack(self):
        self.notifier.post_vulnerabilities(self.url, self.vulnerabilities)

    def _get_scan_result_path(self):
        parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        return os.path.join(parent_dir, self.result_file_name)

    def _get_wp_scan_cmd(self):
        arguments = [
            "--update",
            f"--api-token={self._get_api_token()}",
            "-f json",
            f"-o {self._get_scan_result_path()}",
            f"--url {self.url}"
        ]
        return self.wp_scan_binary_path + " " + " ".join(arguments)

    def scan(self, url):
        """Performs the WP Scan"""
        self.url = url
        sp_result = subprocess.run(self._get_wp_scan_cmd(), shell=True, stdout=subprocess.PIPE)
        results = self._load_scan_result()
        self._parse_vulnerabilities(results)
        self.post_vulnerabilities_to_slack()

    def _load_scan_result(self):
        """Loads the result of the scan"""
        with open(self._get_scan_result_path(), 'r') as file:
            return json.loads(file.read())

    def _get_cve_url(self, cve_id):
        """Returns the URL to a CVE"""
        return f'https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve_id}'

    def _parse_vulnerability(self, vuln_json, **kwargs):
        """Parses and returns a vulnerability object; custom logic from original wpscan"""
        vulnerability = Vulnerability(
            type=kwargs.get('vuln_type'),
            title=vuln_json.get('title', '')
        )
        if 'url' in vuln_json.get('references', ''):
            try:
                vulnerability.set_title_link(vuln_json.get('references', {}).get('url', [])[0])
            except IndexError:
                pass
        if 'cve' in vuln_json.get('references', ''):
            try:
                cve_id = f'CVE-{vuln_json.get("references", {}).get("cve", [])[0]}'
                vulnerability.set_author_name(cve_id)
                vulnerability.set_author_link(self._get_cve_url(cve_id))
            except IndexError:
                pass
        if 'fixed_in' in vuln_json:
            vulnerability.add_field('Fixed Version', vuln_json['fixed_in'])
        if kwargs.get('vuln_type') == 'version':
            number = vuln_json.get('version', {}).get('number', {})
            confidence = vuln_json.get('version', {}).get('confidence', {})
            if number and confidence:
                vulnerability.add_field('Version', f"{number} ({confidence}%)")
        elif kwargs.get('vuln_type') == 'theme':
            number = vuln_json.get('main_theme', {}).get('version', {}).get('number', {})
            confidence = vuln_json.get('main_theme', {}).get('version', {}).get('confidence', {})
            if number and confidence:
                vulnerability.add_field('Version', f"{number} ({confidence}%)")
        elif kwargs.get('vuln_type') == 'plugin':
            number = vuln_json.get('plugins', {}).get('version', {}).get('number', {})
            confidence = vuln_json.get('plugins', {}).get('version', {}).get('confidence', {})
            if number and confidence:
                vulnerability.add_field('Version', f"{number} ({confidence}%)")
        return vulnerability

    def _get_plugin_vulnerabilities(self, results):
        """Returns a list of all plugin vulnerabilities"""
        vulns = []
        try:
            for plugin in results['plugins']:
                try:
                    for result in results['plugins'][plugin]['vulnerabilities']:
                        vulns.append(self._parse_vulnerability(result, vuln_type='plugin'))
                except TypeError:
                    continue
        except TypeError:
            pass
        return vulns

    def _get_theme_vulnerabilities(self, results):
        """Returns a list of all theme vulnerabilities"""
        vulns = []
        try:
            for result in results['main_theme']['vulnerabilities']:
                self.vulnerabilities.append(self._parse_vulnerability(result, vuln_type='theme'))
        except TypeError:
            pass
        return vulns
    
    def _get_wordpress_version_vulnerabilities(self, results):
        """Returns a list of all wordpress version vulnerabilities"""
        vulns = []
        try:
            for result in results['version']['vulnerabilities']:
                self.vulnerabilities.append(self._parse_vulnerability(result, vuln_type='version'))
        except TypeError:
            pass
        return vulns

    def _parse_vulnerabilities(self, results):
        """Parses vulnerabilities from the wpscan output"""
        self.vulnerabilities = self.vulnerabilities + self._get_wordpress_version_vulnerabilities(results)
        self.vulnerabilities = self.vulnerabilities + self._get_theme_vulnerabilities(results)
        self.vulnerabilities = self.vulnerabilities + self._get_plugin_vulnerabilities(results)


if __name__ == "__main__":
    arguments = sys.argv
    fwps = FiixWordPressScanner()
    fwps.scan(arguments[1])
