from bs4 import BeautifulSoup
import mechanize, csv, requests, urllib2
import pandas as pd

br = mechanize.Browser()
url = 'http://download.bls.gov/pub/time.series/'
br.open(url)
html = br.response().read()
soup = BeautifulSoup(html)

links = soup.findAll('a')

goodlinks = []

for link in links:
    if 'series' in link['href']:
        goodlinks.append('http://download.bls.gov' + link['href'])

def DownloadFile(url, filename):
    req = urllib2.urlopen(url)
    CHUNK = 16 * 1024
    with open(filename, 'wb') as fp:
      while True:
        chunk = req.read(CHUNK)
        if not chunk: break
        fp.write(chunk)
    return

def convertFile(filename):
    f = open(filename)
    outputFile = filename[:-4] + '.csv'
    o = open(outputFile, 'wb')
    writer = csv.writer(o)
    while True:
        row = f.readline().strip().split('\t')
        if row == ['']:
            break
        writer.writerow(row)
    o.close()
    return outputFile

d = pd.DataFrame()

##goodlinks = goodlinks[:2]
##print goodlinks

for link in goodlinks:
    br.open(link)
    soup = BeautifulSoup(br.response().read(), 'lxml')
    links2 = soup.findAll('a')
    goodlinks2 = []

    for link2 in links2:
        if 'series' in link2['href']:
            goodlinks2.append('http://download.bls.gov' + link2['href'])

    for url in goodlinks2:
        if url.endswith('series'):
            break
        
    filename = url.split('/')[-1] + '.txt'
    
    
    DownloadFile(url, filename)
    
    outputFile = convertFile(filename)
    df = pd.read_csv(outputFile)
    columns = list(df.columns)
    for col in columns:
        if '_code' in col:
            get_data = col.split('_')[0]
            for l in goodlinks2:
                if l.endswith(get_data):
                    break
            url = l
            #print url
            filename2 = url.split('/')[-1] + '.txt'
            #print filename2
            if filename2 not in ['bg.measure.txt', 'bg.unit.txt', 'bg.alteration.txt',\
                                 'bg.sector.txt', 'bp.measure.txt']:
                DownloadFile(url, filename2)
                #print 'Downloading', filename2
            outputFile2 = convertFile(filename2)
            df1 = pd.read_csv(outputFile2)
            if  'footnote' in col:
                df1.columns = ['footnote_codes', 'footnote_text']
            elif 'measure' in col:
                df1.columns = ['measure_code', 'Measure']
            try:
                df = pd.merge(df, df1, on = col, how = 'left')
            except Exception,e:
                print 'issue with', filename2
                
            #print df.shape

    
    #d = pd.concat([d,df], axis=0)

d.to_csv('2_ap_bd.csv')
