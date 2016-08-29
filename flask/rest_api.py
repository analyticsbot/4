#!flask/bin/python
## importing all required modules
from flask import Flask, jsonify, request
import pandas as pd
from sklearn import linear_model
import numpy as np
from itertools import combinations

## initialize the flask app
app = Flask(__name__)
app.secret_key = "/\xfa-\x84\xfeW\xc3\xda\x11%/\x0c\xa0\xbaY\xa3\x89\x93$\xf5\x92\x9eW}"

def equationsLR(filename, numEqn):
    """Function to take the csv file, return the set of equations
        filename = csv input file
        numEqn = number of equations to be returned back
    """
    ## read the csv file and pop the output variable to a y variable
    X = pd.read_csv(filename)
    y = X.pop('PNL')

    ## take out all columns for multiple equations
    columns = list(X.columns)

    ## get all possible combinations
    all_combinations = []

    for i in range(0, len(columns)+1):
        for subset in combinations(columns, i):
               if len(subset)!=0:
                   all_combinations.append(list(subset))

    ## intialize a dictionary to store the equations
    equations = {}
    count = 0

    for comb in all_combinations:
        X_temp = X[comb]
        # Create linear regression object
        regr = linear_model.LinearRegression()

        # Train the model using the training sets
        regr.fit(X_temp, y)

        # The coefficients
        coef = list(regr.coef_)

        # construct linear equations
        eqn = ''
        for el in coef:
            ix = coef.index(el)
            if el>=0.0:
                eqn =  eqn + ' + ' + comb[ix]+'*'+str(abs(el)) 
            else:
                eqn =  eqn + ' - ' + comb[ix]+'*'+str(abs(el))
        eqn = eqn.strip()[1:].strip()

        equations[count] = eqn
        count+=1
        if count>int(numEqn):
            break

    return equations
        

@app.route('/getEquations', methods=['GET'])
def getEquations():
    """ GET view to request the equations
    sample request = http://127.0.0.1:5000/getEquations?csvFile=data.csv&numEqn=10
    """
    csvFile = request.args.get('csvFile')
    numEqn = request.args.get('numEqn')

    eqns = equationsLR(csvFile, numEqn)
    
    return jsonify({'eqns': eqns})

if __name__ == '__main__':
    ## debug = True. Show errors
    app.run(debug=True)
