url = 'http://download.bls.gov/pub/time.series/ch/ch.series'
import urllib2
req = urllib2.urlopen(url)
CHUNK = 16 * 1024
with open('ch.series.txt', 'wb') as fp:
  while True:
    chunk = req.read(CHUNK)
    if not chunk: break
    fp.write(chunk)
