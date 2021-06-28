# WPScan docker action

Scan a URL with `wpscan`, a WordPress vulnerability scanner. JSON scan results are returned to the next step and/or sent to Slack.

https://wpscan.com/


## Inputs

### `url`

**Required**. Scan target URL.

### `token`

API token for wpscan.com. Required for vulnerability data.

### `options`

WPScan CLI options.  Default `--disable-tls-checks`.

### `webhook`

Slack webhook URL.

### `webhookevent`

Events to send webhook on: Default `vulns,aborted`. Allowed `vulns,aborted,completed`.

## Outputs

### `result`

JSON scan results.

### `resultb64`

JSON scan results, base64 encoded.

## Example usage

```yaml
uses: WTFender/wpscan-action
with:
  url: 'https://WORDPRESS_SITE/'
  token: ${{ secrets.WPSCAN_TOKEN }}
  webhook: ${{ secrets.SLACK_WEBHOOK }}
```