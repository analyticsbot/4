from bs4 import BeautifulSoup
import mechanize, csv, requests, urllib2, urllib, sqlalchemy, os
import pandas as pd

connection_string = "DRIVER={SQL Server};SERVER=WIN-VVBB3KC93CA;UID=RaviShankar;PWD=MaYHcorporation2015;DATABASE=BLS;"
connection_string = urllib.quote_plus(connection_string) 
connection_string = "mssql+pyodbc:///?odbc_connect=%s" % connection_string
engine = sqlalchemy.create_engine(connection_string)
connection = engine.connect()
##fetch columns
meta = sqlalchemy.MetaData(bind=engine, reflect=True)

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
connection.execute("use bls;")
goodlinks.remove('http://download.bls.gov/pub/time.series/esbr/')
goodlinks = goodlinks[:1]
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

    '''
    
    if filename not in ['ln.series.txt']:
        outputFile = convertFile(filename)
    elif filename == 'ln.series.txt':
        outputFile = 'ln.series.csv'
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
                                 'bg.sector.txt', 'bp.measure.txt',\
                                 'ln.series.txt']:
                DownloadFile(url, filename2)
                #print 'Downloading', filename2
            
            outputFile2 = convertFile(filename2)
##            df1 = pd.read_csv(outputFile2)
##            if  'footnote' in col:
##                df1.columns = ['footnote_codes', 'footnote_text']
##            elif 'measure' in col:
##                df1.columns = ['measure_code', 'Measure']
##            try:
##                df = pd.merge(df, df1, on = col, how = 'left')
##            except Exception,e:
##                print 'issue with', filename2
##                
##            #print df.shape
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
connection.close()
#d.to_csv('2_ap_bd.csv')
'''
