##from sqlalchemy import create_engine
##engine = create_engine("mssql://RaviShankar:MaYHcorporation2015@74.63.228.198/bls")
##for row in engine.execute("select user_id, user_name from users"):
##    print row.user_id, row.user_name
import urllib, sqlalchemy
import pandas as pd

connection_string = "DRIVER={SQL Server};SERVER=WIN-VVBB3KC93CA;UID=Administrator;PWD=yFybBrEMMrt3Z7Dr;DATABASE=BLS"
connection_string = "DRIVER={SQL Server};SERVER=WIN-VVBB3KC93CA;UID=RaviShankar;PWD=MaYHcorporation2015;DATABASE=BLS;"

connection_string = urllib.quote_plus(connection_string) 
connection_string = "mssql+pyodbc:///?odbc_connect=%s" % connection_string
#connection_string = "mssql+pyodbc://RaviShankar:MaYHcorporation2015@WIN-VVBB3KC93CA/bls"
print connection_string
engine = sqlalchemy.create_engine(connection_string)
connection = engine.connect()

df = pd.DataFrame({'Color': ['Red', 'Red', 'Blue'], 'State': ['MA', 'PA', 'PA']})
df1 = pd.DataFrame({'Color1': ['Red', 'Red', 'Blue'], 'State2': ['MA', 'PA', 'PA']})

connection.execute("use bls;")
df.to_sql(name='sample_table3', con=engine, if_exists = 'append', index=False, schema = 'dbo', flavor = 'mssql')

##fetch columns
meta = sqlalchemy.MetaData(bind=engine, reflect=True)
results = meta.tables['sample_table3']

existing_cols = []

for col in results.c:
    existing_cols.append( col)

columns = df1.columns
for c in columns:
    if c not in existing_cols:
        query = "ALTER TABLE sample_table3 ADD " + c + " VARCHAR(500);"
        connection.execute(query)

df1.to_sql(name='sample_table3', con=engine, if_exists = 'append', index=False, schema = 'dbo', flavor = 'mssql')
#connection.execute("CREATE TABLE persons3(id INT, name VARCHAR(100))")
connection.close()
