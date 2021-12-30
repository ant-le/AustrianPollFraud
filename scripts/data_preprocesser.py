
import logging
import re
import pandas as pd
import numpy as np
import pathlib

class Preprocesser:
    """
    Preprocess Data for Analysis
    """
    
    def __init__(self, df=None, wiki=True):
        self.df = df
        self.wiki = wiki
               
               
    def update(self, df, wiki=False):
        self.df = df
        self.wiki = wiki


    def load(self):
        if self.wiki is False:
            self.limit_cases()
            self.recode_columns()
        self.define_columns()
        
        return self.df


    def define_columns(self):
        
        self.df.reset_index(inplace=True)
    
        if self.wiki is True:
            self.df=self.df.drop(df.index[0])
            
            # Change values for Wikipedia
                # Find rows with interval estimation
                # Extract numbers and compute the mean
                # cast to float and potentially safe integer
            
            cols_dic = {
                "ÖVP":"ÖVP",
                "SPÖ":"SPÖ",
                "FPÖ":"FPÖ",
                "Grüne":"Grüne",
                "Polling firm": "Institute",
                "End date": "Date",
            }
            
        if self.wiki is False:
            cols_dic = {
                "ovp":"ÖVP",
                "spo":"SPÖ",
                "fpo":"FPÖ",
                "gru":"Grüne",
                "institut":"Institute",
                "datum":"Date",
            }

        self.df = self.df[list(cols_dic.keys())]
        self.df = self.df.rename(columns=cols_dic)
                
        # Changing dtype of column
        for var in ["ÖVP", "SPÖ", "FPÖ", "Grüne"]:
            self.df[var] = pd.to_numeric(self.df[var], downcast='integer')
        
        self.df["Date"] = pd.to_datetime(self.df["Date"])
            
        # Recode institute to binary var
        self.df["Institute_bin"] = np.where(self.df["Institute"].str.contains("Research Affairs"),1,0)
                
        logging.info("Variables recoded sucessfully!")
            

    def limit_cases(self):
        var = ["regionID", "datum"]
        self.df[var[0]] = pd.to_numeric(self.df[var[0]], downcast='integer')
        self.df = self.df[self.df[var[0]]==1]
        
        self.df[var[1]] = pd.to_datetime(self.df[var[1]])
        self.df = self.df[self.df[var[1]].dt.year == 2017]
        logging.info("Cases limited!")


    def recode_columns(self):
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