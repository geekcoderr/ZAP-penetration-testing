#!/usr/bin/env python
from weasyprint import HTML
import time
from zapv2 import ZAPv2
import requests

# The URL of the application to be tested
target = 'http://192.168.244.209/portal.php'
# Change to match the API key set in ZAP, or use None if the API key is disabled
apiKey = 'ma3mg1658sb23o3ejc6o8k1tra'
zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8081', 'https': 'http://127.0.0.1:8081'})

# Authentication
login_url = "http://192.168.244.209/login.php"
payload = {
    "login": "bee",
    "password": "bug",
    "security_level": "0",
    "form": "submit"
}

response = requests.post(login_url, data=payload)

if "Which bug do you want to hack today" in response.text:
    print("Logged in")

    # Spidering target
    print('Spidering target {}'.format(target))
    scanID = zap.spider.scan(target)
    while int(zap.spider.status(scanID)) < 100:
        print('Spider progress %: {}'.format(zap.spider.status(scanID)))
        time.sleep(1)

    print('Spider has completed!')
    print('\n'.join(map(str, zap.spider.results(scanID))))

    # Scanning target
    print('Scanning target {}'.format(target))
    scanID = zap.ascan.scan(target)
    while int(zap.ascan.status(scanID)) < 100:
        print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
        time.sleep(1)

    print('Scan has completed')

    # Generate an HTML report
    print('Generating HTML Report')
    report_html = zap.core.htmlreport()
    with open('Spider_zap_report.html', 'w', encoding='utf-8') as f:
        f.write(report_html)

    print('HTML Report generated: Spider_zap_report.html')

    # Convert the HTML report to a PDF
    print('Converting HTML report to PDF')
    HTML(string=report_html).write_pdf('Spider_zap_report.pdf')

    print('PDF Report generated: Spider_zap_report.pdf')
else:
    print("Login failed")
