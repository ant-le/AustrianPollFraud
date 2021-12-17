
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime as dt
import pathlib

from scripts.config import Directory

class Handler:
    """
    
    """
    def __init__(self, df):
        self.df = df
        
        
    def fixed_effects(self):
        pass
        #y = b0 + b1*resaff + b2*kurz + b3*kurz*resaff + Monats-FEs; Darstellung sind avg. marginal effects von resaff bei kurz==0 und kurz==1)
    
    
    def plotDifference(self, var, save=False):
        self.df = self.df[self.df.Date.dt.year==2017]
        with plt.style.context('bmh'):
            fig, ax = plt.subplots(figsize=(11,5))
            ax.scatter("Date", var, data=self.df[self.df["Institute_bin"]==1], label="Research Affairs", c='orange')
            ax.scatter("Date", var, data=self.df[self.df["Institute_bin"]==0], label="Other Institutes", c='royalblue')
            ax.set_ylabel("Percentage Points")
            ax.axvline(dt.datetime(2017, 5, 10), c='grey', ls="--", label="Leadership Change")
            #ax.axvline(dt.datetime(2016, 12, 8), c='grey', ls="--", label="National Election Date")
            ax.legend(fancybox=True)
            ax.set_title('Gap between polls between survey institutes in voting share of ' + str(var))
            myFmt = mdates.DateFormatter('%m/%Y')
            ax.xaxis.set_major_formatter(myFmt)
            ax.tick_params(axis='x', labelrotation = 45)
            plt.show()
            
            if save is True:
                directory = Directory()
                path = directory.imageFolder().joinpath(str(var) + "_difference.jpg")
                fig.savefig(path, dpi=300)
        
        
    def naive_dif_in_dif(self, var, plot=True, save=False):
        after = self.df[(self.df["Date"] >= dt.datetime(2017,5,10)) & (self.df["Date"].dt.year == 2017)].groupby("Institute_bin")[var].mean()
        before = self.df[(self.df["Date"] < dt.datetime(2017,5,10)) & (self.df["Date"].dt.year == 2017)].groupby("Institute_bin")[var].mean()
        diff_in_diff = (after.loc[1] -before.loc[1])-(after.loc[0]-before.loc[0])
        print("Naive Diff-in-Diff Estimator of changes in " + str(var) + ": ")
        print("[E(Y1|D=1)-E(Y1|D=0)] - [E(Y0|D=1)-E(Y0|D=0)] = "+ str(diff_in_diff))
        
        
        if plot is True:
            with plt.style.context('ggplot'):
                fig, ax = plt.subplots(figsize=(10,5))
                ax.plot(["Jan-May", "May-December"], [before.loc[1], after.loc[1]], label="Research Affairs", lw=2)
                ax.plot(["Jan-May", "May-December"], [before.loc[0], after.loc[0]], label="Other Institutes", lw=2)
                ax.plot(["Jan-May", "May-December"], [before.loc[1], before.loc[1] +(after.loc[0]-before.loc[0])], label="Counterfactual", lw=2, color="C2", ls="-.")
                ax.set_ylabel("Percentage Points")
                ax.legend(fancybox=True)
                ax.set_title("Plot of Counterfacutals of Naive Diff-in-Diff Estimator")
                plt.show()
        
        if save is True:
            directory = Directory()
            path = directory.imageFolder().joinpath(str(var) + "_causal_estimate.jpg")
            fig.savefig(path, dpi=300)            

        
        
        
        
if __name__ == "__main__":
    Plotter = Plotter()
    df = plotter.scatterplot()