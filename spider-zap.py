#!/usr/bin/env python
from weasyprint import HTML
import time
from zapv2 import ZAPv2


# The URL of the application to be tested
target = 'http://192.168.43.228/portal.php/'
# Change to match the API key set in ZAP, or use None if the API key is disabled
apiKey = 'f7j5imf51q5qbcrdsi3bgguj36'
# zap=ZAPv2(apikey=apiKey)
# By default ZAP API client will connect to port 8080
zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8081', 'https': 'http://127.0.0.1:8081'})

print('Spidering target {}'.format(target))
# The scan returns a scan id to support concurrent scanning
scanID = zap.spider.scan(target)
while int(zap.spider.status(scanID)) < 100:
    # Poll the status until it completes
    print('Spider progress %: {}'.format(zap.spider.status(scanID)))
    time.sleep(1)

print('Spider has completed!')
# Prints the URLs the spider has crawled
print('\n'.join(map(str, zap.spider.results(scanID))))

# Perform an Active Scan (optional)
print('Scanning target {}'.format(target))
scanID = zap.ascan.scan(target)
while int(zap.ascan.status(scanID)) < 100:
    print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
    time.sleep(1)

print('Scan has completed!')

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
