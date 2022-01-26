
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
from datetime import datetime


class Plotter:
    """
    Hallo  
    """
    
    def __init__(self, var="ÖVP", intervention=datetime(2017,5,10)):
        self.var = var
        self.intervention = intervention
    

    def scatter(self, df, save=False):
        df = df.copy()
        months = df.Date.dt.strftime("%b").unique()
        df["Institute"] = np.where(df["Institute"].str.contains("Research Affairs"),1,0)

        with plt.style.context('seaborn-darkgrid'):
            fig, ax = plt.subplots(figsize=(10,5))
            ax.scatter("Date", self.var, data=df[df["Institute"]==1], 
                       label="Research Affairs", c='sandybrown', s=25)
            ax.scatter("Date", self.var, data=df[df["Institute"]==0], 
                       label="Other Institutes", c='royalblue', s=25)
            ax.axvline(self.intervention, c='lightgrey', ls="--", label="Leadership Change")
            ax.legend(fancybox=True)
            ax.set(xticklabels=months)  
            ax.set_xlabel("Date")
            ax.set_ylabel("Estimated Voting % or " + str(self.var))
            ax.set_title("Descriptive Plot of Data")
            plt.show()
            
            if save is True:
                path = Path(__file__).parent.parent / "images" / "descriptive.csv"
                fig.savefig(path, dpi=300)
           
           
if __name__ == "__main__":
    pass