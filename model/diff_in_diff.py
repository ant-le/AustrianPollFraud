
from cgi import test
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from scipy import stats

class TwoWayFixedEffects:
    """
    Implementation of canonical Difference-in-Difference Design with a 
    Two-Way-Fixed-Effects Estimator where Ordinary Least Squares (OLS) 
    is used to fit a linear regression model to the data. The coefficients 
    beta = (beta_0, ..., beta_p) minimise the residual sum of squares between 
    the observed targets in the dataset and the targets predicted by the 
    linear approximation. The standard errors of the FE linear approximation only 
    hold for the 2*2 case of a canonical design.
    
    Parameters
    ----------
    intervention : datetime, default=dt.datetime(2017,5,10)
        This parameter desices which date will be used for splitting the units
        into pre-intervention Group and post-intervention group.
    var : String, default='ÖVP'
        Determines the dependent variable of the model. Alternatively 'SPÖ',
        'FPÖ' or 'Grüne' can be stated.
    test: String, default='t'
        Determines based on which distribution the standard errors will be 
        computed. For using the Standard Normal Distribution input 'z' to
        account for population data without (sampling) estimation error.
        
    Attributes
    ----------
    fit : df of shape (n_features, n_summaryStatistics)
        pd.DataFrame containing all relevant summary statistics. Depending on furhter
        specification hypothesis testing might be included or not.
    """

    def __init__(self, intervention=datetime(2017,5,10), var='ÖVP', test='t'):
        self.intervention = intervention
        self.var = var
        self.test = test
    

    def fit(self, df):
        """
        Linear approximation of the Two-Way Fixed Effects (causal) effect with 
        beta = (beta_0, ..., beta_p) being the parameters minimising the residual
        sum of squares based on an input pd.DataFrame and the relevant information
        stated in the constructor.
        
        Parameters
        ----------
        df : df of shape (n_units, n_features)
            Input DataFrame containing (at least) all relevant varialbes necessary for
            analysis.
        var_names list of length 2, default=["Date", "Institute"]
            Names of varaibles used for the fixed effects linear regression model. The
            interaction term is calculated manually.
        """
        df = df.copy()
        df["Intercept"] = np.hstack([np.ones(len(df))]) 
        keep = ["Intercept", "Treatment", "Intervention", "DiD"]
        X = df[keep].values
        y = df.loc[:, self.var].values
        
        # Computing the Estimates 
        invs_gram = np.linalg.inv(X.T @ X)
        moment = X.T @ y
        betas = invs_gram @ moment
        
        # Computing the Standard Error
        df = X.shape[0]
        if self.test == 't':
            df -= X.shape[1]        
        
        yhat = X @ betas
        error = np.subtract(y, yhat)
        mse = np.divide(error.T @ error, df)
        se = np.sqrt(mse * invs_gram.diagonal())
                        
        # Construct Confidence Intervals
        # Do I need t-Test or not?
        t_CI = 1.96
        if self.test == 't':
            t_CI = stats.t.ppf(0.975 ,df)

        lower = betas - t_CI * se
        upper = betas + t_CI * se 
        
        # Hypothesis Testing
        score = np.divide(betas,se)
        p = 2*stats.norm.sf(abs(score))
        if self.test == 't':
            p = 2*(1-stats.t.cdf(score, df))

        
        # t = np.divide(self.betas, errors)
        self.fit = pd.DataFrame(list(zip(betas, se, score, p, lower, upper)), 
                                    columns=['Coef', 'SE', f'{self.test}', 'p-value', '2.5% CI', '97.5% CI'], 
                                    index=["Intercept", "Institute", "Time Intervention", "Diff-in-Diff"])
        logging.info("OLS Regression successful!")
        

    def summary(self, latex=False, plot=False):
        """
        Summary Statistics of the linear (tow-way FE) regression model. 
        
        Parameters
        ----------
        latex : bool, default=False
            Whether summary statistics should be returned as table or as tabular embedded
            in latex code.
        plot bool, default=False
            Whether result of Diff-in-Diff design should be illustrated graphically. Possibly 
            standard errors will also be used for the illustration of uncertainty levels.
        """
        if isinstance(self.fit, pd.DataFrame):
            if latex:
                print(self.fit.drop(columns=[f'{self.test}', 'p-value']).round(decimals=3).to_latex(caption="Output of Two-Way Fixed Effects OLS Linear Regression Model",
                    label="TWFE_Output", position="h!"))
            else:
                print("_______________________________________________________________")
                print(self.fit.drop(columns=[f'{self.test}', 'p-value']))
                print("_______________________________________________________________")
            
            if plot:
                values = self.fit.loc[:, "Coef"]
                              
                with plt.style.context('ggplot'):
                    fig, ax = plt.subplots(figsize=(10,5))
                    ax.plot(["Jan 1 - May 10", "May 11 - October 9"], 
                               [values[:2].sum(), values.sum()], 
                               label="Research Affairs", lw=2, c="sandybrown")
                    ax.plot(["Jan 1 - May 10", "May 11 - October 9"], 
                               [values[0], values[[0,2]].sum()], 
                               label="Other Institutes", lw=2, c="royalblue")
                    ax.plot(["Jan 1 - May 10", "May 11 - October 9"], 
                               [values[:2].sum(), values[:3].sum()], 
                               label="Counterfactual", lw=2, color="darkgrey", ls="-.")
                    ax.set_ylabel("Percentage Points of " + str(self.var))
                    ax.legend(fancybox=True)
                    ax.set_title("Plot of Counterfacutals of Naive Diff-in-Diff Estimator")
                    plt.show()
                    
        else:
            print("No Estimates are computed yet")            
    
if __name__ == "__main__":
    pass