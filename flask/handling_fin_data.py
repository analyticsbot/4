import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
from sklearn.cross_validation import cross_val_predict
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
from sklearn.metrics import r2_score

X = pd.read_csv('data.csv')
y = X.pop('PNL')

columns = list(X.columns)

all_combinations = []

for i in range(0, len(columns)+1):
    for subset in combinations(columns, i):
           if len(subset)!=0:
               all_combinations.append(list(subset))


for comb in all_combinations:
    print comb
    X_temp = X[comb]
    # split into a training and testing set
    X_train, X_test, y_train, y_test = train_test_split(
        X_temp, y, test_size=0.25, random_state=42)

    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(X_train, y_train)

    # The coefficients
    print('Coefficients: \n', regr.coef_, '\n')
    y_pred = regr.predict(X_test)
    print r2_score(y_test, y_pred) 
