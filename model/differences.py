
from distutils.log import error
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from scipy import stats

class Diff_in_Diff_Model():
    def __init__(self, intervention=dt.datetime(2017,5,10), var="ÖVP"):
        self.intervention = intervention
        self.var = var
        
        
    def fitData(self, df):
        df["Intervention"] = np.where(df["Date"] < self.intervention, 0, 1)
        df["DiD"] = df["Treatment"] * df["Intervention"]
        keep = ["Treatment", "Intervention", "DiD"]
        
        self.x = df.loc[:, keep]
        self.y = df.loc[:, self.var]
    

    def ols_regression(self):
        # Reshaping the Data
        x = np.hstack([np.ones(len(self.x))[:, np.newaxis], self.x])
        y = self.y.values
        
        # Computing the Estimates 
        invs_gram = np.linalg.inv(x.T @ x)
        moment = x.T @ y
        betas = invs_gram @ moment
        
        # Computing the Standard Error
        df = x.shape[0] - x.shape[1]
        yhat = x @ betas
        error = np.subtract(y, yhat)
        mse = np.divide(error.T @ error, df)
        se = np.sqrt(mse * invs_gram.diagonal())
                        
        # Construct Confidence Intervals
        t = stats.t.ppf(0.975 ,df)
        lower = betas - t * se
        upper = betas + t * se 
        
        # Hypothesis Testing
        # t = np.divide(self.betas, errors)
        self.results = list(zip(betas, se, lower, upper))
        

    def summary(self, latex=False):
        if self.results:
            df = pd.DataFrame(self.results, 
                  columns=["Coef", "SE", "2.5% CI", "97.5% CI"], 
                  index=["Intercept", "Institute", "Time Intervention", "Diff-in-Diff"])
            if latex:
                print(df.to_latex(caption="Diff-in-Diff Linear Regression Outpit",
                    label="Diff_in_Diff", position="h!"))
            else:
                print(df)
        else:
            error("No Results are generated yet")
    