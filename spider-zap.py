#!/usr/bin/env python
import time
from zapv2 import ZAPv2

# The URL of the application to be tested
target = 'http://192.168.43.228/portal.php/'
# Change to match the API key set in ZAP, or use None if the API key is disabled
apiKey = 'pdks9l01m832fn5ao8nj4lmlsg'

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
