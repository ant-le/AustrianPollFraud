
import numpy as np
from numpy.linalg import svd
import datetime as dt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

"""
DID is implemented as an interaction term between 
time and treatment group dummy variable.
"""
def diff_in_diff_regression(x, y, summary=True):
    if summary:
        # Statsmodels
        X2 = sm.add_constant(x)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print(est2.summary())
    else:
        # SkLearn
        model = LinearRegression()
    
        model.fit(x, y)
        difference = model.coef_[2]
        return difference