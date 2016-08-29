from bs4 import BeautifulSoup
import mechanize, csv, requests
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
    r = requests.get(url)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
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

goodlinks = goodlinks[:2]
print goodlinks

for link in goodlinks:
    br.open(link)
    soup = BeautifulSoup(br.response().read(), 'lxml')
    links2 = soup.findAll('a')
    goodlinks2 = []

    for link2 in links2:
        if 'series' in link2['href']:
            goodlinks2.append('http://download.bls.gov' + link2['href'])

    for url in goodlinks2:
        if 'data.' in url: 
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
                    filename2 = url.split('/')[-1] + '.txt'
                    DownloadFile(url, filename2)
                    outputFile2 = convertFile(filename2)
                    df1 = pd.read_csv(outputFile2)
                    if  'footnote' in col:
                        df1.columns = ['footnote_codes', 'footnote_text']
                    df = pd.merge(df, df1, on = col, how = 'left')
                    print df.shape

        
            d = pd.concat([d,df], axis=0)

d.to_csv('2_ap_bd_data.csv')
