import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
from sklearn.cross_validation import cross_val_predict
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import LinearSVC


X = pd.read_csv('data.csv')
y = X.pop('PNL')

# split into a training and testing set
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

# Create linear regression object
model = LinearSVC()

# Train the model using the training sets
model.fit(X_train, y_train)

# The coefficients
print('Coefficients: \n', model.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(X_test) - y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(X_test, y_test))

# Plot outputs
plt.scatter(X_test, y_test,  color='black')
plt.plot(X_test, regr.predict(X_test), color='blue',
         linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()
