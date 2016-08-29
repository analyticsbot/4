import pandas as pd
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
from sklearn.cross_validation import cross_val_predict
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
from sklearn.metrics import r2_score
import dateutil
import statsmodels.formula.api as smf

df = pd.read_csv('outputabc.csv')
dates = list(df['GRID_MTH_DT'].unique())

columns  = list(df['IDX_NM'].unique()) + ['GRID_MTH_DT', 'PNL']
new_df = pd.DataFrame(columns = columns)
monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

i = 0
for d in dates:
    temp = df[df['GRID_MTH_DT'] == d]
    curve_nms = list(df['CURVE_NM'].unique())
    for curve in curve_nms:
        temp_new = temp[temp['CURVE_NM'] == curve]
        #print temp.shape, d

        INPUT_PR_AMT = list(temp_new['INPUT_PR_AMT'])
        INPUT_PR_AMT = [float(f) for f in INPUT_PR_AMT]
        new_df.loc[i] = INPUT_PR_AMT + list(temp_new['GRID_MTH_DT'].unique())\
                        + [float(list(temp_new['PNL'].unique())[0])]
        i+=1
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

for d in dates:
    X = new_df[new_df['GRID_MTH_DT'] == d]
    grid_date = X.pop('GRID_MTH_DT')
    gf = dateutil.parser.parse(grid_date.values[0])
    gf_text = monthDict[gf.month]+'_'+str(gf.year)
    #y = X.pop('PNL')
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
        if 'PNL' not in comb:
            continue
        if len(comb)==1 and  'PNL'  in comb:
            continue
        if len(comb)< len(new_col_x)*.9:
            continue
        X_temp = X[comb]
        formula_x = ' + '.join(comb)
        formula = 'PNL ~ ' + formula_x
        lm = smf.ols(formula, data=X_temp).fit()

        xx = lm.params.to_dict()
        yy = X_temp.to_dict()

        eqn = ''
        
        for key, value in xx.iteritems():
            if key !='Intercept':
                    if value>=0.0:
                            eqn =  eqn + ' + ' + str(key)+'*'+str(abs(value))+'*'+gf_text
                    else:
                            eqn =  eqn + ' - ' + str(key)+'*'+str(abs(value))+'*'+gf_text

        eqn = eqn.strip()[1:].strip()
        if xx['Intercept']>0.0:
            eqn = eqn + ' + ' + str(abs(xx['Intercept']))
        else:
            eqn = eqn + ' - ' + str(abs(xx['Intercept']))
        print eqn
        print getR2(xx, yy)
                                
   



    
