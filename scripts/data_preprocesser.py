
import logging
import re
import pandas as pd
from pandas.api.types import is_string_dtype
import numpy as np
import pathlib

from scripts.config import Configurator

class Preprocesser:
    """
    Preprocess Data for Analysis
    """
    
    def __init__(self, df=None, url=None):
        self.df = df
        self.url = url
        self.configurator = Configurator()
               
               
    def update(self, df, url):
        self.df = df
        self.url = url
        

    def load(self):
        self.limit_cases()
        self.recode_columns()
        self.define_columns()
        
        return self.df


    def define_columns(self):
        
        self.df.reset_index(inplace=True)
    
        if "wiki" in self.url:
            self.df=self.df.drop(df.index[0])
            cols_dic = {
                "ÖVP":"ÖVP",
                "SPÖ":"SPÖ",
                "FPÖ":"FPÖ",
                "Grüne":"Grüne",
                "Polling firm": "Institute",
                "End date": "Date",
            }  
        elif "neuwal" in self.url:
            cols_dic = {
                "ovp":"ÖVP",
                "spo":"SPÖ",
                "fpo":"FPÖ",
                "gru":"Grüne",
                "institut":"Institute",
                "datum":"Date",
                "n":"Sample Size"
            }
        elif "strategie" in self.url:
            cols_dic = {
                "oevp":"ÖVP",
                "spoe":"SPÖ",
                "fpoe":"FPÖ",
                "gruene":"Grüne",
                "institute":"Institute",
                "date":"Date",
                "sample":"Sample Size"
            }
        elif "polyd" in self.url:
            cols_dic = {
                "OEVP":"ÖVP",
                "SPOE":"SPÖ",
                "FPOE":"FPÖ",
                "GRUENE":"Grüne",
                "firm":"Institute",
                "date":"Date",
                "n":"Sample Size",
                "sd": "Sampling Variance"
            }
              
    

        self.df = self.df[list(cols_dic.keys())]
        self.df = self.df.rename(columns=cols_dic)
                
        # Changing dtype of column
        keep = ["ÖVP", "SPÖ", "FPÖ", "Grüne"]
        if "Sample Size" in self.df.columns:
            keep.append("Sample Size")
        if "Sampling Variance" in self.df.columns:
            keep.append("Sampling Variance")
        
        
        for var in keep:
            if is_string_dtype(self.df[var]):
                self.df[var] = self.df[var].str.replace(",", ".")
                self.df[var] = pd.to_numeric(self.df[var])
        
        self.df["Date"] = pd.to_datetime(self.df["Date"])
 
        # Recode institute to binary var
        self.df["Institute_bin"] = np.where(self.df["Institute"].str.contains("Research Affairs"),1,0)
                
        logging.info("Variables recoded sucessfully!")
            

    def limit_cases(self):
        if "wiki" not in self.url:
            var = []
            if "neuwal" in self.url:
                var.extend(["datum", "regionID"])
                self.df[var[1]] = pd.to_numeric(self.df[var[1]], downcast='integer')
                self.df = self.df[self.df[var[1]]==1]
                
            elif "strategie" or "polyd" in self.url:
                var.append("date")

            self.df[var[0]] = pd.to_datetime(self.df[var[0]])
            self.df = self.df[self.df[var[0]].dt.year == 2017]
            
        logging.info("Cases limited!")


    def recode_columns(self):
        if "neuwal" in self.url:
            # Recode Voting Percentages
            cols = [x for x in self.df.columns if re.search("Css", x)]
            for col in cols:
                parties = self.df[col].unique()
                
                for party in parties:
                    if party not in self.df.columns:
                        self.df[party] = np.nan
                        
                    self.df.loc[(self.df[col] == party), party] = self.df.loc[(self.df[col] == party), col[0:2]+"Value"]
                
        logging.info("Columns recoded successfully!")


if __name__ == "__main__":
    pass