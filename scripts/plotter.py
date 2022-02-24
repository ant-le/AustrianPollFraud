
from os import access
import matplotlib.pyplot as plt
import arviz as az
import xarray as xr
from pathlib import Path


class Plotter:
    
    def __init__(self, var="ÖVP"):
        self.var = var
    

    def scatter(self, df, save=False):
        df = df.copy()
        months = df.Date.dt.strftime("%b").unique()
        with plt.style.context('seaborn-darkgrid'):
            fig, ax = plt.subplots(figsize=(10,5))
            ax.scatter("Date", self.var, data=df[df["Institute"]==1], 
                       label="Research Affairs", c='sandybrown', s=25)
            ax.scatter("Date", self.var, data=df[df["Institute"]==0], 
                       label="Other Institutes", c='royalblue', s=25)
            ax.axvline(dt.datetime(2017,5,10), c='lightgrey', ls="--", label="Leadership Change")
            ax.legend(fancybox=True)
            ax.set(xticklabels=months)  
            ax.set_xlabel("Date")
            ax.set_ylabel("Estimated Voting % or " + str(self.var))
            ax.set_title("Descriptive Plot of Data")
            plt.show()
            
            if save is True:
                path = Path(__file__).parent.parent / "images" / "descriptive.csv"
                fig.savefig(path, dpi=300)
           
    
    def compare_models(self, model1, model2, kind='forestplot'):
        # Rename Betas
        posterior1 = az.convert_to_inference_data(model1.fit)
        posterior2 = az.convert_to_inference_data(model2.fit)

        with az.style.context("arviz-whitegrid"):
            fig = plt.figure(figsize=(13, 5), constrained_layout=True)
            spec = fig.add_gridspec(2, 3)
            ax0 = fig.add_subplot(spec[0, :])
            az.plot_forest(
                [posterior1, posterior2], 
                model_names=["Imputation Model", "Naive Model"], 
                var_names=["beta"],
                kind=kind,
                combined=False,
                ridgeplot_overlap=1.1,
                figsize=(9, 4),
                ax=ax0
            )
            ax0.set_yticklabels([]) 
            ax0.set_title("99% Interval", fontsize=10)

            ax10 = fig.add_subplot(spec[1, 0])
            ax11 = fig.add_subplot(spec[1, 1])
            ax12 = fig.add_subplot(spec[1, 2]) 
            ax=[ax10,ax12,ax11] 
            az.plot_density([posterior1, posterior2], 
                data_labels=["Imputation Model", "Naive Model"], 
                var_names="beta",
                bw=.99,
                ax=ax
            )
            for axs, name in zip(ax, ["Group", "DiD", "Time"]):
                print(axs)
                axs.set_title("")
                axs.set_xlabel(name)
            ax10.get_legend().remove()
            fig.suptitle("Overview over Results of Bayesian Regression Models", fontsize=20)
            plt.show()
            
            
    def plot_posterior(self, model):
        posterior = az.convert_to_inference_data(model.fit)
        with az.style.context("arviz-whitegrid"):
            az.plot_posterior(posterior, 
                              var_names="beta",
                              show=True,
                              ref_val=[-1.78, 13.92, 5.85]
                              )


if __name__ == "__main__":
    pass