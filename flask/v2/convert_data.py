import pandas as pd
import dateutil.parser
from sklearn.cross_validation import train_test_split
from sklearn.metrics import r2_score
from sklearn import linear_model
from sklearn.feature_selection import SelectKBest
from sklearn import feature_selection as fs

df = pd.read_csv('output_new_format.csv' )
df['grid_col'] = df.apply (lambda row: row['IDX_NM'] + ' ' + str(dateutil.parser.parse(row['GRID_MTH_DT']).strftime('%Y_%d')),axis=1)
eods = list(df['EOD'].unique())

i=0
for eod in eods:
    temp = df[df['EOD'] == eod]
    columns = list(temp['grid_col'])
    new_columns = []
    for col in columns:
        new_columns.append(col.replace(' ', '_').replace('.',''))
    new_columns += ['PNL']
    INPUT_PR_AMT = list(temp['INPUT_PR_AMT'])
    PNL = list(temp['PNL'].unique())

    if i == 0:
        new_df = pd.DataFrame(columns = new_columns)
    values = INPUT_PR_AMT + PNL
    value_dict = {}
    for new_col in new_columns:
        ix = new_columns.index(new_col)
        value_dict[new_col] = values[i]
    new_df.loc[i] = values
    i+=1
equations = {}
num_features = len(new_df.columns)
columns1 = new_df.columns
y = new_df.pop('PNL')
for i in range(1, num_features):
    b = fs.SelectKBest(fs.f_regression, k=i)
    X = b.fit_transform(new_df, y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    regr = linear_model.LinearRegression(fit_intercept = True, n_jobs = -1)
    regr.fit(X_train, y_train)
    
    index_taken = list(b.get_support())
    variables_taken = []
    for j in range(len(index_taken)):
        if index_taken[j] == True:
            variables_taken.append(columns1[j])
    
    y_pred = regr.predict(X_test)
    #print variables_taken, list(regr.coef_),
    r2_value = r2_score(y_test, y_pred)

    coef = list(regr.coef_)
    eqn = ''
    for el in coef:
        ix = coef.index(el)
        if el>=0.0:
            eqn =  eqn + ' + ' + str(abs(el)) +'*' + variables_taken[ix]
        else:
            eqn =  eqn + ' - ' + str(abs(el)) +'*' + variables_taken[ix]

    eqn = eqn.strip()[1:].strip()
    if regr.intercept_>=0.0:
        eqn = eqn + ' + ' + str(abs(regr.intercept_))
    else:
        eqn = eqn + ' - ' + str(abs(regr.intercept_))
    equations['eqn_'+str(i)] = {'equation':eqn, 'r2_score':r2_value}

numEqn = 10
count = 0
equations_sorted = sorted(equations.items(),key=lambda x: x[1]['r2_score'],reverse=True)
new_equations = {}
for eqn_new in equations_sorted:
    new_equations[eqn_new[0]] = eqn_new[1]
    count+=1
    if count>int(numEqn):
        break
print new_equations
