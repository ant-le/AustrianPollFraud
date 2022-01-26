
import logging
import pandas as pd
import datetime as dt
from pathlib import Path

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
      
    def __init__(self, df=None, date=dt.datetime(2017,10,15)):
        self.df = df
        self.date = date
        self.path = Path(__file__).parent.parent / "data"
    
    
    def loadProcessed(self):
        path = self.path / "analysis" / "au_polls.csv"
        self.df = pd.read_csv(path)
        self.df['Date'] = pd.to_datetime(self.df.Date)
        return self.df


    def load(self, save=False, scraper=None):
        if scraper:
            self.df = scraper.load()
        else:
            path = self.path / "raw" / "polls.csv"
            self.df = pd.read_csv(path)
            logging.info("Data loaded successfully!")
                
        self.df = self._preprocessing()
        self.df = self._modify()        
        logging.info(f"Data preprocessed successfully!")

        if save:
            path = self.path / "analysis" / "au_polls.csv"
            self.df.to_csv(path)
            
        return self.df
    
    
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