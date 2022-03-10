
from cProfile import label
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import arviz as az
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import timedelta


class Plotter:
    
    def __init__(self):
        pass


    def scatter(self, df, save=False, var='ÖVP', binning=True):
        df = df.copy()        
        with plt.style.context('ggplot'):
            fig, ax = plt.subplots(figsize=(14,5))
            ax.scatter("Date", var, data=df[df["Treatment"]==1], 
                       label="Research Affairs", 
                       s=25,
                       c='olive',
                       alpha=.6
            )
            ax.scatter("Date", var, data=df[df["Treatment"]==0], 
                       label="Other Institutes",
                       s=25,
                       c='silver',
                       alpha=.6

            )
            if binning:
                # Create Lines seperating bins
                upper = df.groupby('bins')['Date'].max()[:-1].reset_index(drop=True)
                lower = df.groupby('bins')['Date'].min()[1:].reset_index(drop=True)
                bins = lower + (upper - lower)/2              
                ax.vlines(bins, ymin=df[var].min()-1, ymax=df[var].max()+1, color='black',lw=.5)
                
                # Plotting mean value of each bin with fixed distances
                pos = []
                pos.append(df.Date.min()-timedelta(5))
                pos[1:len(bins)] = bins
                pos.append(df.Date.max()+timedelta(5))
                for b in df.bins.unique():
                    ax.hlines(df.loc[(df.bins==b) & (df.Treatment==1), var].mean(),
                              xmin=pos[b-1]+timedelta(7),
                              xmax=pos[b]-timedelta(7),
                              color="olive",
                    )
                    ax.hlines(df.loc[(df.bins==b) & (df.Treatment==0), var].mean(),
                              xmin=pos[b-1]+timedelta(5),
                              xmax=pos[b]-timedelta(5),
                              color='silver',
                    )
            ax.set_xlim([df.Date.min()-timedelta(20), df.Date.max()+timedelta(20)])
            ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
            ax.xaxis.set_minor_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
            ax.set_ylim(df[var].min()-2, df[var].max()+2)    
            ax.set_ylabel("Estimated Voting % for " + str(var))
            ax.legend(fancybox=True)
            plt.show()
            if save is True:
                path = Path(__file__).parent.parent / "images" / "descriptive.csv"
                fig.savefig(path, dpi=300)
    
    
    def trends(self, df, var='ÖVP', error=True, diff=.1):            
        df = df.copy() 
        tg = df[df.Treatment==1].groupby('bins')[var].mean().values   
        cg = df[df.Treatment==0].groupby('bins')[var].mean().values   
        with plt.style.context('ggplot'):  
            _, ax = plt.subplots(1,1,figsize=(10,5))
            if error:
                ax.errorbar(df.bins.unique()+diff,
                            tg, 
                            df[df.Treatment==1].groupby('bins')[var].std().values,
                            elinewidth=.7,
                            color='olive',
                            #alpha=.6,
                            fmt='o',
                            capsize=6,
                            label='Research Affairs'
                )
                ax.errorbar(df.bins.unique()-diff,
                            cg, 
                            df[df.Treatment==0].groupby('bins')[var].std().values,
                            elinewidth=.7,
                            color='silver',
                            fmt='o',
                            capsize=6,
                            label='Other Institutes'
                )
                
            else:          
                ax.scatter(x=df.bins.unique()+diff, y=tg,
                        label="Research Affairs", 
                        s=25,
                        c='olive',
                        alpha=.6
                )
                ax.scatter(x=df.bins.unique()-diff, y=cg,
                            label="Other Institutes",
                            s=25,
                            facecolors=None, 
                            edgecolors='k', 
                            c='silver',
                            lw=1.2,
                            alpha=.6)
            ax.legend(fancybox=True)
            ticks = ['-3', '-2', '-1', '0', '1', '2', '3', '4', '5']
            plt.xticks(np.r_[1:10], ticks)
            ax.set_ylabel("Estimated Voting % for " + str(var))
            ax.set_title("Pre-trends based on binning")
            plt.show()


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
            for axs, name in zip(ax, ["Group", "Time", "DiD"]):
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
    df = pd.read_csv("/Users/anton/Documents/University/Semester_7/Bachelor_Thesis/data/analysis/polls.csv")
    df.rename(columns={'datum':'Date'}, inplace=True)
    df["Date"] = pd.to_datetime(df.Date)
    plotter = Plotter()
    plotter.trends(df, var="SPÖ")