from bs4 import BeautifulSoup
import mechanize, csv, requests, urllib2, urllib, sqlalchemy, os
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
    if not os.path.isfile(filename):
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
goodlinks.remove('http://download.bls.gov/pub/time.series/esbr/')
goodlinks = goodlinks[:3]
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
    i=0
    while True:
        if i == 0:
            header=0
            skip=0
        else:
            header=None
            skip=1

        df = pd.read_csv(filename, sep = '\t', nrows = 10, skiprows = 10*i+skip, header = header)

        if i == 0:
            columns = list(df.columns)
        else:
            df.columns = columns
        i+=1

        if df.shape[0] == 0 or i ==2:
            break

        #print df

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
                if filename2 not in [] : #['bg.measure.txt', 'bg.unit.txt', 'bg.alteration.txt',\
                                       #'bg.sector.txt', 'bp.measure.txt',\
                                     #'ln.series.txt']
                    DownloadFile(url, filename2)
                    #print 'Downloading', filename2
                
                outputFile2 = convertFile(filename2)
                df1 = pd.read_csv(outputFile2)
                if df1.shape[1] == 1:
                    print filename2
                    continue
                if  'footnote' in col:
                    df1.columns = ['footnote_codes', 'footnote_text']
                elif 'measure' in col:
                    df1.columns = ['measure_code', 'Measure']
                try:
                    df = pd.merge(df, df1, on = col, how = 'left')
                except Exception,e:
                    print 'issue with', filename2
                
            #print df.shape
##
##    ##fetch columns
##    results = meta.tables['sample_table3']
##    existing_cols = []
##
##    for col in results.c:
##        existing_cols.append( col)
##
##    columns = df.columns
##    for c in columns:
##        if c not in existing_cols:
##            query = "ALTER TABLE sample_table3 ADD " + c + " VARCHAR(500);"
##            try:
##                connection.execute(query)
##            except:
##                pass
    #df.to_sql(name='sample_table3', con=engine, if_exists = 'append', index=False, schema = 'dbo', flavor = 'mssql')

    
    #d = pd.concat([d,df], axis=0)
#connection.close()
#d.to_csv('2_ap_bd.csv')

