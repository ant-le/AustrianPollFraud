
import logging
import matplotlib.pyplot as plt
import matplotlib.dates
import seaborn as sns

class Plotter:
    """
    
    """

    def __init__(self, df):
        self.df = df
        
        
    def scatterplot(self, var):
        plt.scatter("Date", var, c="Institute_bin", data=self.df)
        plt.xlabel('Date')
        plt.ylabel("Percentage Points")
        plt.show()
        

if __name__ == "__main__":
    Plotter = Plotter()
    df = plotter.scatterplot()
