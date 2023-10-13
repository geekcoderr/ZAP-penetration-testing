#!/usr/bin/env python
from weasyprint import HTML
import time
from zapv2 import ZAPv2


target = 'http://192.168.43.228/portal.php/'
# Change to match the API key set in ZAP, or use None if the API key is disabled
apiKey = 'f7j5imf51q5qbcrdsi3bgguj36'
# zap=ZAPv2(apikey=apiKey)
# By default ZAP API client will connect to port 8080
zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8081', 'https': 'http://127.0.0.1:8081'})


print('Ajax Spider target {}'.format(target))
scanID = zap.ajaxSpider.scan(target)

timeout = time.time() + 60*2   # 2 minutes from now
# Loop until the ajax spider has finished or the timeout has exceeded
while zap.ajaxSpider.status == 'running':
    if time.time() > timeout:
        break
    print('Ajax Spider status' + zap.ajaxSpider.status)
    time.sleep(2)

print('Ajax Spider completed')
ajaxResults = zap.ajaxSpider.results(start=0, count=10)


# Generate an HTML report
print('Generating HTML Report')
report_html = zap.core.htmlreport()
with open('zap_report.html', 'w', encoding='utf-8') as f:
    f.write(report_html)

print('HTML Report generated: Spider_zap_report.html')

# Convert the HTML report to a PDF
print('Converting HTML report to PDF')
HTML(string=report_html).write_pdf('Spider_zap_report.pdf')

print('PDF Report generated: zap_report.pdf')
