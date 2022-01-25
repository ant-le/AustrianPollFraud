
from distutils.log import error
import imp
from charset_normalizer import logging
import numpy as np
import pandas as pd
import datetime as dt
import colorsys
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as cl
from scipy import stats

class Diff_in_Diff_Model():
    """
    Ordinary least squares Difference-in-Differences Regression.
    LinearRegression fits a linear model with coefficients beta = (beta_0, ..., beta_p)
    to minimise the residual sum of squares between the observed targets in
    the dataset, and the targets predicted by the linear approximation.
    Parameters
    ----------
    intervention : datetime, default=dt.datetime(2017,5,10)
        This parameter desices which date will be used for splitting the units
        into pre-intervention Group and post-intervention group.
    var : String, default='ÖVP'
        Determines the dependent variable of the model. Alternatively 'SPÖ',
        'FPÖ' or 'Grüne' can be stated.
    Attributes
    ----------
    x : df of shape (n_units, n_features)
        Matrix X
    y : array of shape (n_units, 1)
        Vector with the values of the dependent variable 
    """

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
        """
        Methods to fit linear model with coefficients beta = (beta_0, ..., beta_p)
        minimising the residual sum of squares with beta = (X^T*X)^-1 * X*y.
        """
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
        self.results = pd.DataFrame(list(zip(betas, se, lower, upper)), 
                                    columns=["Coef", "SE", "2.5% CI", "97.5% CI"], 
                                    index=["Intercept", "Institute", "Time Intervention", "Diff-in-Diff"])
        
        logging.info("OLS Regression successful!")
        

    def summary(self, latex=False, plot=False):
        if isinstance(self.results, pd.DataFrame):
            if latex:
                print(self.results.to_latex(caption="Diff-in-Diff Linear Regression Output",
                    label="Diff_in_Diff", position="h!"))
            else:
                print("_______________________________________________________________")
                print(self.results)
                print("_______________________________________________________________")
            if plot:
                values = self.results.loc[:, "Coef"]                  
                with plt.style.context('ggplot'):
                    fig, ax = plt.subplots(2, 1, figsize=(10,5))
                    ax.plot(["Jan 1 - May 10", "May 11 - October 9"], 
                               [values[:2].sum(), values.sum()], 
                               label="Research Affairs", lw=2, c="sandybrown")
                    ax.plot(["Jan 1 - May 10", "May 11 - October 9"], 
                               [values[0], values[[0,2]].sum()], 
                               label="Other Institutes", lw=2, c="royalblue")
                    ax.plot(["Jan 1 - May 10", "May 11 - October 9"], 
                               [values[:2].sum(), values[:3].sum()], 
                               label="Counterfactual", lw=2, color="sandybrown", ls="-.")
                    ax.set_ylabel("Percentage Points of " + str(self.var))
                    ax.legend(fancybox=True)
                    ax.set_title("Plot of Counterfacutals of Naive Diff-in-Diff Estimator")
                    plt.show()
                    
        else:
            error("No Estimates are computed yet")            
    
if __name__ == "__main__":
    pass