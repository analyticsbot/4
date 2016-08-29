import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

x = 10 * np.random.random(100)
z = 20 * np.random.random(100)
y = -4 + 2 * x + 3*z

model = make_pipeline(PolynomialFeatures(2), Ridge(alpha=1E-8, fit_intercept=False))
model.fit(x[:, None], y)
ridge = model.named_steps['ridge']
print(ridge.coef_)
# array([-4.,  2., -3.])
