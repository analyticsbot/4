import dateutil, sqlalchemy, dateutil, urllib
import pandas.io.sql as psql
import pandas as pd
##connection_string = "DRIVER={SQL Server};SERVER=primeonedev.cloudapp.net;UID=sa;PWD=Rt%^DCime17;DATABASE=Primeone;"
##connection_string = urllib.quote_plus(connection_string) 
##connection_string = "mssql+pyodbc:///?odbc_connect=%s" % connection_string
##engine = sqlalchemy.create_engine(connection_string)
##connection = engine.connect()
##meta = sqlalchemy.MetaData(bind=engine, reflect=True)
##ScenarioSetId = 7
##sql = "SELECT [CURVE_ID],[CURVE_NM],[IDX_NM],[GRID_MTH_DT],[INPUT_PR_AMT],[PNL],[ScenarioSetId]FROM [PrimeOne].[dbo].[VW_MLScenarioSetProdCurveDetail]   where ScenarioSetId = %d" % (int(ScenarioSetId)) 
##df = psql.read_sql(sql, connection)
##df.to_csv('outputabc.csv')
df = pd.read_csv('output_new.csv')
print '***', df.shape
#df['GRID_MTH_DT'] = df['GRID_MTH_DT'].apply(lambda x: str(dateutil.parser.parse(x).strftime('%Y/%m/%d')))
df['GRID_MTH_DT'] = df['GRID_MTH_DT'].apply(lambda x: str(dateutil.parser.parse(x).strftime('%Y/%m/%d')))
print 'colums1', list(df.columns)
dates = list(df['GRID_MTH_DT'].unique())
print dates

columns  = list(df['IDX_NM'].unique()) + ['GRID_MTH_DT', 'PNL']
print 'colu2', columns
new_df = pd.DataFrame(columns = columns)
monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

i = 0
equations = {}
count = 0
for d in dates:
    temp = df[df['GRID_MTH_DT'] == d]
    curve_nms = list(df['CURVE_NM'].unique())
    for curve in curve_nms:
        temp_new = temp[temp['CURVE_NM'] == curve]
        #print temp.shape, d
        #[float(list(temp['PNL'].unique())[0])]

        INPUT_PR_AMT = list(temp_new['INPUT_PR_AMT'])
        INPUT_PR_AMT = [float(f) for f in INPUT_PR_AMT]
        new_df.loc[i] = INPUT_PR_AMT + list(temp_new['GRID_MTH_DT'].unique())\
                        + [float(list(temp['PNL'].unique())[0])]
        i+=1

new_df.to_csv('output_18_June.csv')
