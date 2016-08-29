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

##goodlinks = goodlinks[:2]
##print goodlinks
goodlinks.remove('http://download.bls.gov/pub/time.series/esbr/')

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

        
##            d = pd.concat([d,df], axis=0)
        ##    ##fetch columns
            try:
                results = meta.tables['sample_data']
                existing_cols = []

                for col in results.c:
                    existing_cols.append( str(col).replace('sample_data.', ''))
            except:
                pass
                existing_cols = []
            

            columns = list(df.columns)
            for c in columns:
                if c not in existing_cols:
                    if c == 'footnote_codes':
                        c = 'footnote_code'
                    if str(df[c].dtype)=='object':
                        query = "ALTER TABLE sample_data ADD " + c + " VARCHAR;"
                    elif str(df['footnote_codes'].dtype)=='float64':
                        query = "ALTER TABLE sample_data ADD " + c + " FLOAT;"
                    elif str(df['footnote_codes'].dtype)=='int64':
                        query = "ALTER TABLE sample_data ADD " + c + " INT;"
                    else:
                        print str(df['footnote_codes'].dtype)
                        query = "ALTER TABLE sample_data ADD " + c + " VARCHAR;"
                    try:
                        connection.execute(query)
                    except:
                        pass
            try:
                df.to_sql(name='sample_data', con=engine, if_exists = 'append', index=False, schema = 'dbo', flavor = 'mssql')
            except Exception,e:
                print outputFile



d.to_csv('2_ap_bd_data.csv')
