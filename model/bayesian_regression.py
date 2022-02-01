
import pystan as ps
import numpy as np
import pandas as pd
from datetime import datetime
import multiprocessing
multiprocessing.set_start_method("fork")

import warnings
warnings.simplefilter('ignore', FutureWarning)


class BayesRegression:
    """
    Bayesian: modeling and imputing missing potential outcomes 
    based on their posterior distributions

    Bayesian inference considers the observed values of the 
    four quantities to be realizations of random variables 
    and the unobserved values to be unobserved random variables
    """
     
    def __init__(self, intervention=datetime(2017,5,10), var="ÖVP"):
        self.intervention = intervention
        self.var = var
        self.model = ps.StanModel(file="model/model.stan", extra_compile_args=["-w"])

    
    def fitData(self, df, num_iter=10000, num_chains=1, num_warmup=1500, num_thin=1):
        df = df.copy()
        df["Treatment"] = np.where(df["Institute"].str.contains("Research Affairs"),1,0)
        df["Intervention"] = np.where(df["Date"] < self.intervention, 0, 1)
        df["DiD"] = df["Treatment"] * df["Intervention"]
        keep = ["Treatment", "Intervention", "DiD"]
        data_dict = {"x": df.loc[:, keep], "y": df.loc[:, self.var], "N": len(df), "K":len(keep)}
        self.fit = self.model.sampling(data=data_dict, 
                                       iter=num_iter, 
                                       chains=num_chains, 
                                       warmup=num_warmup, 
                                       thin=num_thin)
        
        
    def printResults(self, latex=False):
        print(self.fit)
        
        if latex:
            summary_dict = self.fit.summary()
            df_sum = pd.DataFrame(summary_dict["summary"],
                          columns=summary_dict["summary_colnames"],
                          index=summary_dict["summary_rownames"])
            print(df_sum.to_latex(caption="Diff-in-Diff Linear Regression Output",
                    label="Diff_in_Diff", position="h!"))
        # Extracting traces
        df_traces = pd.DataFrame()
        for param in ["alpha", "beta", "sigma", "lp__"]:
            if param is "beta":
                df_traces[[f"{param}_1", f"{param}_2", f"{param}_3"]] = self.fit[param]
            else:
                df_traces[param] = self.fit[param]
                
        
if __name__ == "__main__":
    pass