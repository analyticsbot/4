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

df = pd.read_csv('ML Use Case 1-Saif.csv')
dates = list(df['GRID_MTH_DT'].unique())

columns  = list(df['IDX_NM'].unique()) + ['GRID_MTH_DT', 'PNL']
new_df = pd.DataFrame(columns = columns)

i = 0
for d in dates:
    temp = df[df['GRID_MTH_DT'] == d]
    #print temp.shape, d

    INPUT_PR_AMT = list(temp['INPUT_PR_AMT'])
    INPUT_PR_AMT = [float(f) for f in INPUT_PR_AMT]
    new_df.loc[i] = INPUT_PR_AMT + list(temp['GRID_MTH_DT'].unique())\
                    + [float(list(temp['PNL'].unique())[0].replace('$','').replace(',',''))]
    i+=1

for i, row in new_df.iterrows():
    b = new_df.loc[i].to_dict()
    X =pd.DataFrame(b, index = [0])
    y = X.pop('PNL')
    month = X.pop('GRID_MTH_DT')

    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(X, y)

    # The coefficients
    print month
    print('Coefficients: \n', regr.coef_, '\n')
    y_pred = regr.predict(X)
    print r2_score(y_pred, y) 
