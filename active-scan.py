#!/usr/bin/env python
from weasyprint import HTML
import time
from pprint import pprint
from zapv2 import ZAPv2



# The URL of the application to be tested
target = 'http://192.168.43.228/portal.php/'
# Change to match the API key set in ZAP, or use None if the API key is disabled
apiKey = 'f7j5imf51q5qbcrdsi3bgguj36'

zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8081', 'https': 'http://127.0.0.1:8081'})


# TODO : explore the app (Spider, etc) before using the Active Scan API, Refer the explore section
print('Active Scanning target {}'.format(target))
scanID = zap.ascan.scan(target)
while int(zap.ascan.status(scanID)) < 100:
    # Loop until the scanner has finished
    print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
    time.sleep(5)

print('Active Scan completed')
# Print vulnerabilities found by the scanning
print('Hosts: {}'.format(', '.join(zap.core.hosts)))
print('Alerts: ')
pprint(zap.core.alerts(baseurl=target))

# Generate an HTML report
print('Generating HTML Report')
report_html = zap.core.htmlreport()
with open('active-scan_zap_report.html', 'w', encoding='utf-8') as f:
    f.write(report_html)

print('HTML Report generated: active-scan_zap_report.html')

# Convert the HTML report to a PDF
print('Converting HTML report to PDF')
HTML(string=report_html).write_pdf('active-scan_zap_report.pdf')

print('PDF Report generated: active-scan_zap_report.pdf')