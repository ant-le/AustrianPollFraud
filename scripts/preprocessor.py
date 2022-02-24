
import logging
import pandas as pd
import datetime as dt
from pathlib import Path
import numpy as np

from data.raw.polls import _urls, _dates, _new_entries, _sample_size
from pandas.api.types import is_string_dtype

class Preprocessor:
    """
    Class preparing all datasets for the analysis. 
    Parameters
    ----------
    date : datetime, default=dt.datetime(2017,10,15)
        This parameter desices which the time-frame which will be analysed. 
    df : String, default=None
        Dataset 
    """
      
    def __init__(self, kind="processed", date=dt.datetime(2017,10,15), intervention=dt.datetime(2017,5,10)):
        self.date = date
        self.kind = kind
        self.intervention = intervention
        self.path = Path(__file__).parent.parent / "data"
    

    def load(self, scraper, save=False):
        if "processed" in self.kind:
            path = self.path / "analysis" / "au_polls.csv"
            self.df = pd.read_csv(path)
            self.df['Date'] = pd.to_datetime(self.df.Date)
            
            
        else:
            if "scrape" in self.kind:
                self.df = scraper.load()
            if "raw" in self.kind:
                path = self.path / "raw" / "polls.csv"
                self.df = pd.read_csv(path)
                logging.info("Data loaded successfully!")
                    
            self.df = self._preprocessing()
            self.df = self._modify()   
            logging.info(f"Data preprocessed successfully!")

        if save:
            path = self.path / "analysis" / "au_polls.csv"
            self.df.to_csv(path)
        
        self.df = self.createVars()      

        return self.df
    
    
    def createVars(self):
        df = self.df.copy()

        df["ÖVP-SPÖ"] = df.ÖVP - df.SPÖ
        df["Treatment"] = np.where(df["Institute"].str.contains("Research Affairs"),1,0)
        df["Intervention"] = np.where(df["Date"] < self.intervention, 0, 1)
        df["DiD"] = df["Treatment"] * df["Intervention"]
        return df
        
    
    def _preprocessing(self):
        df = self.df.copy()
        
        df['date'] = pd.to_datetime(df['date'])
        df = df[df['date'].dt.year == 2017]
        df = df[df['date'] < self.date]
        
        cols_dic = {
            "date":"Date",
            "firm":"Institute",
            "OEVP":"ÖVP",
            "SPOE":"SPÖ",
            "FPOE":"FPÖ",
            "GRUENE":"Grüne",
            "n":"Sample Size",
            "source": "url"
        }
        df = df[list(cols_dic.keys())]
        df = df.rename(columns=cols_dic)
        
        for var in ["ÖVP", "SPÖ", "FPÖ", "Grüne", "Sample Size"]:
            if is_string_dtype(df[var]):
                df[var] = df[var].str.replace(",", ".")
            df[var] = pd.to_numeric(df[var])
                
        df.sort_values(by=['Date', "Institute"], inplace=True, ignore_index=True)

        return df


    def _modify(self):
        df = self.df.copy()
        df.reset_index(drop=False, inplace=True)
        
        entry = _new_entries()
        df.loc[len(df.index)] = entry

        urls = _urls()
        df.loc[df["index"].isin(urls["index"]) , 'url'] = urls.loc[urls["index"].isin(df["index"]), "url"].values

            
        samples = _sample_size()
        df.loc[df["index"].isin(samples["index"]) , 'Sample Size'] = samples.loc[samples["index"].isin(df["index"]), "Sample Size"].values

        
        dates = _dates()
        df.loc[df["index"].isin(dates["index"]) , 'Date'] = dates.loc[dates["index"].isin(df["index"]), "Date"].values

        df.dropna(subset=['url'], inplace=True)
            
        df.sort_values(by=['Date', "Institute"], inplace=True, ignore_index=True)
        df.drop(columns="index")
        return df
    

if __name__ == "__main__":
    pass