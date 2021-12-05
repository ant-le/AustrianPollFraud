
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime as dt
import pathlib

from scripts.config import Directory

class Plotter:
    """
    
    """

    def __init__(self, df):
        self.df = df
        
        
    def scatterplot(self, var, save=False):
        with plt.style.context('bmh'):
            fig, ax = plt.subplots(figsize=(11,5))
            ax.scatter("Date", var, marker=6, data=self.df[self.df["Institute_bin"]==1], label="Research Affairs", c='yellow')
            ax.scatter("Date", var, marker=6, data=self.df[self.df["Institute_bin"]==0], label="Other Institutes", c='purple')
            ax.set_ylabel("Percentage Points")
            ax.axvline(dt.datetime(2017, 5, 10), c='grey', ls="--", label="Leadership Change")
            ax.legend(fancybox=True)
            ax.set_title('Gap between polls between survey institutes')
            myFmt = mdates.DateFormatter('%m/%Y')
            ax.xaxis.set_major_formatter(myFmt)
            ax.tick_params(axis='x', labelrotation = 45)
            plt.show()
            
            if save is True:
                directory = Directory()
                path = directory.imageFolder().joinpath(str(var) + "_difference.jpg")
                fig.savefig(path, dpi=300)
        
                
if __name__ == "__main__":
    Plotter = Plotter()
    df = plotter.scatterplot()
