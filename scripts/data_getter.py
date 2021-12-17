
import pathlib
from numpy import empty
import pandas as pd

from scripts.data_scraper import Scraper
from scripts.config import Directory
from scripts.data_preprocesser import Preprocesser

class Getter:
    """
    get Data
    """ 
    
    def __init__(self):
        self.df = ""
        
    
    def getRawData(self, scrape=False):
        if scrape is True:
            scraper = Scraper()
            self.df = scraper.load()
        
        else:
            directory = Directory()
            path = directory.rawFolder() / "polls.csv"
            self.df = pd.read_csv(path)
            
            
    def getProcessedData(self, scrape=False):
        if scrape is False:
            directory = Directory()
            path = directory.analysisFolder() / "au_polls.csv"
            self.df = pd.read_csv(path)
            self.df["Date"] = pd.to_datetime(self.df["Date"])

        else:
            scraper = Scraper()
            self.df = scraper.load()  
            preprocesser = Preprocesser(self.df)
            preprocesser.load()
            self.df = preprocesser.df
                        
                        
    def writeRawData(self):
        directory = Directory()
        path = directory.rawFolder() / "polls.csv"
        self.df.to_csv(path, index=False)

        
    def writeProcessedData(self):
        directory = Directory()
        path = directory.analysisFolder() / "au_polls.csv"
        self.df.to_csv(path, index=False)
        
    
    def getCheckData(self):
        scraper = Scraper()
        self.df = scraper.load2()
        rename_dic={
            "institute": "institut",
            "oevp": "ovp",
            "spoe": "spo",
            "fpoe": "fpo",
            "gruene": "gru",
            "sample": "n",
            "date": "datum",
        }
        self.df = self.df.rename(columns=rename_dic)
        self.df["regionID"] = 1
        preprocesser = Preprocesser(self.df)
        preprocesser.load()
        self.df = preprocesser.df
        
        