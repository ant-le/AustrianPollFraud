
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime as dt
import numpy as np
import pathlib

from model.diff_in_diff_model import diff_in_diff_regression
from scripts.config import Configurator

class Handler:
    """
    
    """
    def __init__(self, df=None):
        self.df = df
        
        
    def update(self, df):
        self.df = df
    
        
    def two_way_FE(self):
        pass
        #y = b0 + b1*resaff + b2*kurz + b3*kurz*resaff + Monats-FEs; Darstellung sind avg. marginal effects von resaff bei kurz==0 und kurz==1)

    
    def plotDifference(self, var="ÖVP", save=False):
        with plt.style.context('bmh'):
            fig, ax = plt.subplots(figsize=(11,5))
            ax.scatter("Date", var, data=self.df[self.df["Institute_bin"]==1], label="Research Affairs", c='darkorange')
            ax.scatter("Date", var, data=self.df[self.df["Institute_bin"]==0], label="Other Institutes", c='royalblue')
            ax.set_ylabel("Percentage Points")
            ax.axvline(dt.datetime(2017, 5, 14), c='grey', ls="--", label="Leadership Change")
            ax.legend(fancybox=True)
            ax.set_title('Gap between elections polls in voting share of ' + str(var))
            myFmt = mdates.DateFormatter('%m/%Y')
            ax.xaxis.set_major_formatter(myFmt)
            ax.tick_params(axis='x', labelrotation = 45)
            plt.show()
            
            if save is True:
                configurator = Configurator()
                path = configurator.imageFolder().joinpath(str(var) + "_difference.jpg")
                fig.savefig(path, dpi=300)
        
        
    def diff_in_diff(self, yname="ÖVP", date=dt.datetime(2017,5,14), treatment="Institute_bin"):
        # Creating variables for regression model
        self.df["time"] = np.where(self.df["Date"] < date, 0, 1)
        self.df["did"] = self.df[treatment] * self.df["time"]
        
        # limiting variables to relevant ones
        keep = [treatment, "time", "did"]
        x = self.df.loc[:, keep]
        y = self.df.loc[:, yname]
        
        diff = diff_in_diff_regression(x, y)
        print(diff)
        
 
    def naive_diff_in_diff(self, var, plot=True, save=False):
        # Yijt = 𝛽0 + 𝛽1Ej + 𝛽2Postt + 𝛽3Ej × Postt + 𝛽4Xijt + 𝜀ijt
        after = self.df[self.df["Date"] >= dt.datetime(2017,5,14)].groupby("Institute_bin")[var].mean()
        before = self.df[self.df["Date"] < dt.datetime(2017,5,14)].groupby("Institute_bin")[var].mean()
        diff_in_diff = (after.loc[1] -before.loc[1])-(after.loc[0]-before.loc[0])
        print("Naive Diff-in-Diff Estimator of changes in " + str(var) + ": ")
        print("[E(Y1|D=1)-E(Y1|D=0)] - [E(Y0|D=1)-E(Y0|D=0)] = "+ str(diff_in_diff))
        
        if plot is True:
            with plt.style.context('ggplot'):
                fig, ax = plt.subplots(figsize=(10,5))
                ax.plot(["Jan-May", "May-December"], [before.loc[1], after.loc[1]], label="Research Affairs", lw=2, c="darkorange")
                ax.plot(["Jan-May", "May-December"], [before.loc[0], after.loc[0]], label="Other Institutes", lw=2, c="royalblue")
                ax.plot(["Jan-May", "May-December"], [before.loc[1], before.loc[1] +(after.loc[0]-before.loc[0])], label="Counterfactual", lw=2, color="sandybrown", ls="-.")
                ax.set_ylabel("Percentage Points")
                ax.legend(fancybox=True)
                ax.set_title("Plot of Counterfacutals of Naive Diff-in-Diff Estimator")
                plt.show()
        
        if save is True:
            configurator = Configurator()
            path = configurator.imageFolder().joinpath(str(var) + "_causal_estimate.jpg")
            fig.savefig(path, dpi=300)           
            
        
if __name__ == "__main__":
    pass