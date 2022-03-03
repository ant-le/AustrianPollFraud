
import pystan as ps
import pandas as pd
import arviz as az
import matplotlib.pyplot as plt
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

    def __init__(self, var="ÖVP", impute=True):
        self.var = var
        if impute:
            self.model = ps.StanModel(file="model/model_impute.stan", extra_compile_args=["-w"])
        else:
            self.model = ps.StanModel(file="model/model.stan", extra_compile_args=["-w"])
    

    def sample(self, df, num_iter=50000, num_chains=3, num_warmup=10000, num_thin=10):
        df = df.copy()
        keep = ["Treatment", "Intervention", "DiD"]
        data_dict = {"x": df.loc[:, keep], "y_obs": df.loc[:, self.var], "N": len(df), "K":len(keep)}
        self.fit = self.model.sampling(data=data_dict, 
                                       iter=num_iter, 
                                       chains=num_chains, 
                                       warmup=num_warmup, 
                                       thin=num_thin,
                                       control=dict(adapt_delta=0.98))            
        

    def summary(self, latex=False, plot=True):
        if self.fit:
            print('_____________________________________________________________')
            summary_dict = self.fit.summary()
            df = pd.DataFrame(summary_dict["summary"],
                            columns=summary_dict["summary_colnames"],
                            index=summary_dict["summary_rownames"])
            df = df[~df.index.str.contains('real')]
            if latex:
                print(df.to_latex(caption="Diff-in-Diff Linear Regression Output",
                        label="Diff_in_Diff", position="h!"))
            else:
                print(self.fit)
            if plot:
                posterior = az.convert_to_inference_data(self.fit)
                with az.style.context("arviz-whitegrid"):     
                    az.plot_trace(posterior, var_names=["alpha", "beta", "sigma"])
                    plt.suptitle("Traces and Posterior Distribution of Parameters", fontsize=20)
                    plt.show()
            print('_____________________________________________________________')
        else:
            print("No Estimates are computed yet")
                        
                        
if __name__ == "__main__":
    pass