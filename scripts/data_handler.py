
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
    def __init__(self, df=None, var="ÖVP"):
        self.df = df
        self.var = var
        
    def update(self, df=None, var=None):
        if df is not None:
            self.df = df
        if var is not None:
            self.var = var
    
        
    def two_way_FE(self):
        pass
        #y = b0 + b1*resaff + b2*kurz + b3*kurz*resaff + Monats-FEs)

    
    def plotData(self, save=False):
        with plt.style.context('bmh'):
            fig, ax = plt.subplots(figsize=(11,5))
            ax.scatter("Date", self.var, data=self.df[self.df["Institute_bin"]==1], label="Research Affairs", c='darkorange')
            ax.scatter("Date", self.var, data=self.df[self.df["Institute_bin"]==0], label="Other Institutes", c='royalblue')
            ax.set_ylabel("Percentage Points of " + str(self.var))
            ax.axvline(dt.datetime(2017, 5, 14), c='grey', ls="--", label="Leadership Change")
            ax.legend(fancybox=True)
            ax.set_title('Gap between elections polls in voting share')
            myFmt = mdates.DateFormatter('%m/%Y')
            ax.xaxis.set_major_formatter(myFmt)
            ax.tick_params(axis='x', labelrotation = 45)
            plt.show()
            
            if save is True:
                configurator = Configurator()
                path = configurator.imageFolder().joinpath(str(self.var) + "_difference.jpg")
                fig.savefig(path, dpi=300)
        
        
    def diff_in_diff(self, date=dt.datetime(2017,5,14), treatment="Institute_bin"):
        # Yijt = 𝛽0 + 𝛽1Ej + 𝛽2Postt + 𝛽3 (Ej × Postt) + 𝜀ijt

        # Creating variables for regression model
        self.df["time"] = np.where(self.df["Date"] < date, 0, 1)
        self.df["did"] = self.df[treatment] * self.df["time"]
        
        # limiting variables to relevant ones
        keep = [treatment, "time", "did"]
        X = self.df.loc[:, keep]
        y = self.df.loc[:, self.var]
        
        diff = diff_in_diff_regression(X, y)
        print(diff)
        
        
    def plotDifference(self, date=dt.datetime(2017,5,14), treatment="Institute_bin", save=False):
        # Yijt = 𝛽0 + 𝛽1Ej + 𝛽2Postt + 𝛽3Ej × Postt + 𝛽4Xijt + 𝜀ijt
        after = self.df[self.df["Date"] >= date].groupby(treatment)[self.var].mean()
        before = self.df[self.df["Date"] < date].groupby(treatment)[self.var].mean()
        difference = before.loc[1] + (after.loc[0] - before.loc[0])

        with plt.style.context('ggplot'):
            fig, ax = plt.subplots(figsize=(10,5))
            ax.plot(["Jan-May", "May-October"], [before.loc[1], after.loc[1]], label="Research Affairs", lw=2, c="darkorange")
            ax.plot(["Jan-May", "May-October"], [before.loc[0], after.loc[0]], label="Other Institutes", lw=2, c="royalblue")
            ax.plot(["Jan-May", "May-October"], [before.loc[1], difference], label="Counterfactual", lw=2, color="sandybrown", ls="-.")
            ax.set_ylabel("Percentage Points of " + str(self.var))
            ax.legend(fancybox=True)
            ax.set_title("Plot of Counterfacutals of Naive Diff-in-Diff Estimator")
            plt.show()
        
            if save is True:
                configurator = Configurator()
                path = configurator.imageFolder().joinpath(str(self.var) + "_causal_estimate.jpg")
                fig.savefig(path, dpi=300)           
            
        
if __name__ == "__main__":
    pass