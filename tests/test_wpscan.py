import os
from wpscan import FiixWordPressScanner


def get_wp_scanner_instance():
    scanner = FiixWordPressScanner()
    scanner = FiixWordPressScanner()
    scanner.result_file_name = 'tests/result.json'
    return scanner

def test_load_scan_result():
    scanner = get_wp_scanner_instance()
    results = scanner._load_scan_result()
    assert results is not None

def test_wp_scan_cmd():
    os.environ['WP_SCAN_API_TOKEN'] = "test"
    scanner = FiixWordPressScanner()
    url = "https://www.fiixsoftware.com/"
    scanner.url = url
    cmd = scanner._get_wp_scan_cmd()
    assert f'--url {url}' in cmd

def test_can_find_all_total_vulnerabilities():
    scanner = get_wp_scanner_instance()
    results = scanner._load_scan_result()
    scanner._parse_vulnerabilities(results)
    assert len(scanner.vulnerabilities) == 2

def test_can_find_all_plugin_vulnerabilities():
    scanner = get_wp_scanner_instance()
    results = scanner._load_scan_result()
    assert len(scanner._get_plugin_vulnerabilities(results)) == 2

def test_can_find_all_theme_vulnerabilities():
    scanner = get_wp_scanner_instance()
    results = scanner._load_scan_result()
    assert len(scanner._get_theme_vulnerabilities(results)) == 0

def test_can_find_all_wordpress_version_vulnerabilities():
    scanner = get_wp_scanner_instance()
    results = scanner._load_scan_result()
    assert len(scanner._get_wordpress_version_vulnerabilities(results)) == 0
