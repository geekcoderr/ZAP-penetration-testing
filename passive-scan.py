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

# TODO : explore the app (Spider, etc) before using the Passive Scan API, Refer the explore section for details
while int(zap.pscan.records_to_scan) > 0:
    # Loop until the passive scan has finished
    print('Records to passive scan : ' + zap.pscan.records_to_scan)
    time.sleep(2)

print('Passive Scan completed')

# Print Passive scan results/alerts
print('Hosts: {}'.format(', '.join(zap.core.hosts)))
print('Alerts: ')
pprint(zap.core.alerts())


# Generate an HTML report
print('Generating HTML Report')
report_html = zap.core.htmlreport()
with open('passive-scan_zap_report.html', 'w', encoding='utf-8') as f:
    f.write(report_html)

print('HTML Report generated: passive-scan_zap_report.html')

# Convert the HTML report to a PDF
print('Converting HTML report to PDF')
HTML(string=report_html).write_pdf('passive-scan_zap_report.pdf')

print('PDF Report generated: passive-scan_zap_report.pdf')