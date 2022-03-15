
import pystan as ps
import pandas as pd
import arviz as az
import numpy as np
import xarray
xarray.set_options(display_style="html")
import multiprocessing
multiprocessing.set_start_method("fork")

import warnings
warnings.simplefilter('ignore', FutureWarning)


class BayesRegression:
    """
    Implementation of Difference-in-Difference Design with a 
    Two-Way-Fixed-Effects Estimator where Markov-Chain-Monte-Carlo
    sampling methods (MCMC) are used in order to generate estimates
    of the causal effect of interest
    
    Parameters
    ----------
    intervention : datetime, default=dt.datetime(2017,5,10)
        This parameter desices which date will be used for splitting the units
        into pre-intervention Group and post-intervention group.
    var : String, default='ÖVP'
        Determines the dependent variable of the model. Alternatively 'SPÖ',
        'FPÖ' or 'Grüne' can be stated.
    impute : bool, default=True
    
    Attributes
    ----------
    model : StanModel 
        It is a stanModel yes
    """

    def __init__(self, var="ÖVP", att=False):
        self.att = att
        if self.att is True:
            self.model = ps.StanModel(file="model/model_att.stan", extra_compile_args=["-w"])
        else:
            self.model = ps.StanModel(file="model/model.stan", extra_compile_args=["-w"])
        self.var = var
    

    def sample(self, df, num_iter=10000, num_chains=3, num_thin=2, num_warmup=500):
        df = df.copy()
        y = df.loc[:, self.var].values

        if self.att:
            # Intercept and unit FE
            df.loc[:, 'Intercept'] = 1
            keep = ['Intercept', 'Treatment', 'bins']
            df = df[keep]
            # Time FE
            for i in df.bins.unique():
                df[f'Group_{i}'] = np.where(df.bins==i,1,0)
            X = df.drop(columns=['Group_1', 'bins']).values         

            # DiD - Coefficients
            D = pd.DataFrame()
            for i in df.bins.unique():
                D[f'Treatment_{i}'] = np.where((df.bins==i) & (df.Treatment==1),1,0)
            D = D.drop(columns=['Treatment_1']).values        
             
            data_dict = {"x": X, 
                "d": D,
                "y_obs": y, 
                "N": len(df), 
                "T": D.shape[1], 
                "K": X.shape[1]
            }
        else:
            data_dict = {"x": df.loc[:, 'Treatment'].values, 
                "y_obs": y, 
                "N": len(df), 
                "T":len(df.bins.unique()), 
                "time":df.loc[:,'bins'].values
            }
        # I can use the same model twice
        self.fit = self.model.sampling(data=data_dict, 
                                       iter=num_iter, 
                                       chains=num_chains, 
                                       warmup=num_warmup, 
                                       thin=num_thin,
                                       control=dict(adapt_delta=0.98),
                                       seed=12345,
                                       init='random')
        self.post = az.convert_to_inference_data(self.fit)         
        

    def summary(self, latex=False):
        if self.fit:
            print('_____________________________________________________________')
            summary_dict = model.fit.summary()
            df = pd.DataFrame(summary_dict["summary"],
                            columns=summary_dict["summary_colnames"],
                            index=summary_dict["summary_rownames"])
            df = df[~df.index.str.contains('real')]
            if latex:
                print(df.to_latex(caption="Diff-in-Diff Linear Regression Output",
                        label="Diff_in_Diff", position="h!"))
            else:
                print(df)
        else:
            print("No Estimates are computed yet")
                        
                        
if __name__ == "__main__":
    pass