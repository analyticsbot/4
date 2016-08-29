#!flask/bin/python
## importing all required modules
from flask import Flask, jsonify, request
import pandas as pd
from sklearn import linear_model
import numpy as np
from itertools import combinations
import dateutil, urllib
from sklearn import linear_model
from itertools import combinations
from sklearn.metrics import r2_score
import dateutil, sqlalchemy, dateutil
import statsmodels.formula.api as smf
import pandas.io.sql as psql
from sklearn.cross_validation import train_test_split

## initialize the flask app
app = Flask(__name__)
app.secret_key = "/\xfa-\x84\xfeW\xc3\xda\x11%/\x0c\xa0\xbaY\xa3\x89\x93$\xf5\x92\x9eW}"

def getR2(xx, yy):
    s = 0
    for key in xx.keys():
        try:
            val1 = float(xx[key])*float(yy[key][0])
            s+=val1
        except:
            pass

    s +=float(xx['Intercept'])
    return min(1 - (yy['PNL'][0] - s)/yy['PNL'][0],1)

def equationsLR(ScenarioSetId, numEqn):
    """Function to take the csv file, return the set of equations
        filename = csv input file
        numEqn = number of equations to be returned back
    """
    connection_string = "DRIVER={SQL Server};SERVER=primeonedev.cloudapp.net;UID=sa;PWD=Rt%^DCime17;DATABASE=Primeone;"
    connection_string = urllib.quote_plus(connection_string) 
    connection_string = "mssql+pyodbc:///?odbc_connect=%s" % connection_string
    engine = sqlalchemy.create_engine(connection_string)
    connection = engine.connect()
    meta = sqlalchemy.MetaData(bind=engine, reflect=True)

    sql = "SELECT [CURVE_ID],[CURVE_NM],[IDX_NM],[GRID_MTH_DT],[INPUT_PR_AMT],[PNL],[ScenarioSetId]FROM [PrimeOne].[dbo].[VW_MLScenarioSetProdCurveDetail]   where ScenarioSetId = %d" % (int(ScenarioSetId)) 
    df = psql.read_sql(sql, connection)
    print '***', df.shape
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

            INPUT_PR_AMT = list(temp_new['INPUT_PR_AMT'])
            INPUT_PR_AMT = [float(f) for f in INPUT_PR_AMT]
            new_df.loc[i] = INPUT_PR_AMT + list(temp_new['GRID_MTH_DT'].unique())\
                            + [float(list(temp['PNL'].unique())[0])]
            i+=1

    for d in dates:
        X = new_df[new_df['GRID_MTH_DT'] == d]
        grid_date = X.pop('GRID_MTH_DT')
        gf = dateutil.parser.parse(grid_date.values[0])
        gf_text = monthDict[gf.month]+'_'+str(gf.year)
        y = X.pop('PNL')
        column_x = X.columns
        new_col_x = []
        for c in column_x:
            new_col_x.append(c.replace('.','').replace(' ','_'))
        X.columns = new_col_x

        ## take out all columns for multiple equations
        columns_1 = list(X.columns)

        ## get all possible combinations
        all_combinations = []
        for i in range(0, len(columns_1)+1):
            for subset in combinations(columns_1, i):
                   if len(subset)!=0:
                       all_combinations.append(list(subset))

        for comb in all_combinations:
            X_temp = X[comb]
            # Create linear regression object

            X_train, X_test, y_train, y_test = train_test_split(X_temp, y, test_size=0.25, random_state=42)
            regr = linear_model.LinearRegression()

            # Train the model using the training sets
            regr.fit(X_train, y_train)
            
            y_pred = regr.predict(X_test)
            r2_value = r2_score(y_test, y_pred)

            # The coefficients
            coef = list(regr.coef_)

            if all(el==0.0 for el in coef):
                continue

            eqn = ''
            
            for key, value in coef:
                ix = coef.index(el)
                if value>=0.0:
                        eqn =  eqn + ' + ' + comb[ix]+'*'+gf_text+'*'+str(abs(value))
                else:
                        eqn =  eqn + ' - ' + comb[ix]+'*'+gf_text+'*'+str(abs(value))

            eqn = eqn.strip()[1:].strip()
            
##            print eqn
##            print getR2(xx, yy)
##            print 'count', count
##            print '\n'
            equations['eqn_'+str(count)] = {'equation':eqn, 'r2_score':r2_value}
            

    equations_sorted = sorted(equations.items(),key=lambda x: x[1]['r2_score'],reverse=True)
    new_equations = {}
    for eqn_new in equations_sorted:
        new_equations[eqn_new[0]] = eqn_new[1]
        count+=1
        if count>int(numEqn):
            return new_equations
            break
    return new_equations
        

@app.route('/getEquations', methods=['GET'])
def getEquations():
    """ GET view to request the equations
    sample request = http://127.0.0.1:5000/getEquations?ScenarioSetId=7&numEqn=10
    """
    ScenarioSetId  = request.args.get('ScenarioSetId')
    numEqn = request.args.get('numEqn')

    eqns = equationsLR(ScenarioSetId , numEqn)
    
    return jsonify({'eqns': eqns})

if __name__ == '__main__':
    ## debug = True. Show errors
    app.run(debug=True)
