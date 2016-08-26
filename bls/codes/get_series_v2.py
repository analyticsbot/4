from bs4 import BeautifulSoup
import mechanize, csv, requests, urllib2, urllib, sqlalchemy, os
import pandas as pd

connection_string = "DRIVER={SQL Server};SERVER=WIN-VVBB3KC93CA;UID=RaviShankar;PWD=MaYHcorporation2015;DATABASE=BLS;"
connection_string = urllib.quote_plus(connection_string) 
connection_string = "mssql+pyodbc:///?odbc_connect=%s" % connection_string
engine = sqlalchemy.create_engine(connection_string)
connection = engine.connect()
##fetch columns
connection.execute("use bls;")
meta = sqlalchemy.MetaData(bind=engine, reflect=True)

br = mechanize.Browser()
url = 'http://download.bls.gov/pub/time.series/'
br.open(url)
html = br.response().read()
soup = BeautifulSoup(html, 'lxml')

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
goodlinks.remove('http://download.bls.gov/pub/time.series/compressed/')
goodlinks.remove('http://download.bls.gov/pub/time.series/overview.txt')
goodlinks.remove('http://download.bls.gov/pub/time.series/sdmx/')
goodlinks.remove('http://download.bls.gov/pub/time.series/nl/')
goodlinks = goodlinks[56:]
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

        try:
            print filename ,   100000*i+skip, header
            df = pd.read_csv(filename, sep = '\t', nrows = 100000, low_memory=False,  skiprows = 100000*i+skip, header = header)
        except Exception,e:
            print 'issue with series file', filename, str(e)
            break
        print filename, df.shape, i
        if df.shape[0] == 0:
            break
        if i == 0:
            i+=1
            columns1 = list(df.columns)
            print 'column1', columns1
        else:
            i+=1
            try:
                df.columns = columns1
                print list(df.columns)
            except Exception,e:
                print 'issue with series file.......', filename, str(e)
                print i, df.columns, '\n', columns1
                break
        
        #print df.columns

        columns = list(df.columns)
        for col in columns:
            if '_code' in col:
                get_data = col.split('_')[0]
                for l in goodlinks2:
                    if l.endswith(get_data):
                        break
                if goodlinks2.index(l) == len(goodlinks2)-1:
                    continue
                url = l
                #print url
                filename2 = url.split('/')[-1] + '.txt'
                #print filename2
##                if filename2 not in [] : #['bg.measure.txt', 'bg.unit.txt', 'bg.alteration.txt',\
##                                       #'bg.sector.txt', 'bp.measure.txt',\
##                                     #'ln.series.txt']
##                    DownloadFile(url, filename2)
##                    #print 'Downloading', filename2
##                                
                outputFile2 = convertFile(filename2)
                df1 = pd.read_csv(outputFile2, error_bad_lines = False)
                #print df1.columns
                if df1.shape[1] == 1:
                    print 'issue with second file', filename2, 'only one column'
                    continue
                
##                elif 'measure' in col:
##                    df1.columns = ['measure_code', 'Measure']
                new_col = [col]
                for nc in df1.columns:
                    if ('_code' in nc) and (nc in columns) :
                        if nc not in new_col:
                            new_col.append(nc)
                if  'footnote' in col:
                    df1.columns = ['footnote_codes', 'footnote_text']
                    new_col = ['footnote_codes']
                if filename2 in ['cd.footnote.txt', 'cf.footnote.txt', 'hc.footnote.txt']:
                    df1.columns = ['footnote_code', 'footnote_text']
                    new_col = ['footnote_code']

                if filename2 == 'fm.forig.txt':
                    new_col = ['forig_code']
                if filename2 == 'fm.frace.txt':
                    new_col = ['frace_code']
                if filename2 == 'gp.area.txt':
                    new_col = ['state_code', 'area_code']
                if filename2 == 'tu.elwho.txt':
                    new_col = ['elwho_code']
                df = pd.merge(df, df1, on = new_col, how = 'left')
                #print df.columns
                
##                try:
##                    df = pd.merge(df, df1, on = col, how = 'left')
##                except Exception,e:
##                    print 'issue with', filename2, str(e), '****', df.shape, df1.shape
##                    
                
        #sprint filename, df.shape

        ##fetch columns
        try:
            results = meta.tables['sample_table3']
            existing_cols = []

            for col in results.c:
                existing_cols.append( col)
        except:
            existing_cols = []

        columns = df.columns
        for c in columns:
            if c not in existing_cols:
                #sprint 'adding column', c
                query = "ALTER TABLE sample_table3 ADD " + c + " VARCHAR(500);"
                try:
                    connection.execute(query)
                except:
                    pass
        try:
            df.to_sql(name='sample_table3', con=engine, if_exists = 'append', index=False, schema = 'dbo', flavor = 'mssql')
            print 'uploaded', df.shape,filename, i, '###################'
        except  Exception, e:
            print str(e), df.shape, filename, i, '**************'

    
    #d = pd.concat([d,df], axis=0)
#connection.close()
#d.to_csv('2_ap_bd.csv')

