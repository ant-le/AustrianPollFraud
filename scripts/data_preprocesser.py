
import logging
import re
import pandas as pd
import numpy as np
import pathlib

class Preprocesser:
    """
    Preprocess Data for Analysis
    """
    
    def __init__(self, df):
        self.df = df
        

    def load(self):
        self.limit_cases()
        self.recode_columns()
        self.define_columns()
        self.compute_differences()

        
    def limit_cases(self):
        var = ["regionID", "datum"]
        self.df[var[0]] = pd.to_numeric(self.df[var[0]], downcast='integer')
        self.df = self.df[self.df[var[0]]==1]
        
        self.df[var[1]] = pd.to_datetime(self.df[var[1]])
        self.df = self.df[(self.df[var[1]].dt.year > 2013) & (self.df[var[1]].dt.year < 2020)]
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
                
        # Recode institute to binary var
        self.df["bin"] = np.where(self.df.institut == "Research Affairs",1,0)
        logging.info("Variables recoded sucessfully!")
    
       
    def define_columns(self):
        # Rename and keep relevant columns
        cols_dic = {
            "ovp":"ÖVP",
            "spo":"SPÖ",
            "fpo":"FPÖ",
            "gru":"Grüne",
            "institut":"Institute",
            "bin":"Institute_bin",
            "n":"Sample Size",
            "datum":"Date",
            "methode":"Method",
        }
        self.df = self.df[list(cols_dic.keys())]
        self.df = self.df.rename(columns=cols_dic)
        
        # Changing dtype of column
        for var in ["ÖVP", "SPÖ", "FPÖ", "Grüne", "Sample Size"]:
            self.df[var] = pd.to_numeric(self.df[var], downcast='integer')
            
        logging.info("df limited to relevant columns!")
        

    def compute_differences(self):
        self.df["ÖVP_SPÖ"] = self.df["ÖVP"] - self.df["SPÖ"]
        self.df["ÖVP_FPÖ"] = self.df["ÖVP"] - self.df["FPÖ"]
        self.df["ÖVP_Grüne"] = self.df["ÖVP"] - self.df["Grüne"]
        
        
if __name__ == "__main__":
    preprocesser = Preprocesser()
    df = preprocesser.load()