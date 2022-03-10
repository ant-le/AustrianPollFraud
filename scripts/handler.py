
import logging
import re
import pandas as pd
from datetime import datetime
import pathlib
import numpy as np


class Handler:
    """
    Class preparing all datasets for the analysis. 
    Parameters
    ----------
    date : datetime, default=dt.datetime(2017,10,15)
        This parameter desices which the time-frame which will be analysed. 
    df : String, default=None
        Dataset 
    """
      
    def __init__(self, folder='analysis'):
        self.folder = folder
    
        
    def load(self, save=False):
        path = pathlib.Path(__file__).parent.parent / 'data' / f'{self.folder}'

        if self.folder == 'raw':
            self.wiki = pd.read_csv(path.joinpath('wiki.csv'))
            self.neuwal = pd.read_csv(path.joinpath('neuwal.csv'))
            df = self.preprocess()
            
        else:    
            df = pd.read_csv(path.joinpath('polls.csv'))
            df['Date'] = pd.to_datetime(df.Date)

        if save:
            path = pathlib.Path(__file__).parent.parent / 'data' / 'analysis' / 'polls.csv'
            df.to_csv(path, index=False)
            logging.info(f"Data saved!")
            
        logging.info(f"Data processed successfully!")
        return df

        
    def preprocess(self):
        neuwal = self.neuwal.copy()
        neuwal = self._limit(neuwal)
        neuwal = self._recode(neuwal)
        neuwal = self._rename(neuwal)
        neuwal = self._createVars(neuwal)
        
        wiki = self.wiki.copy()
        wiki.rename(columns={'Institut':'Institute','Veröffentlichung':'Date', 'GRÜNE':'Grüne'}, inplace=True)
        wiki['Date'] = pd.to_datetime(wiki.Date, format="%d.%m.%Y")
        wiki = wiki[wiki.Date > datetime(2020,6,14)]
        wiki = self._createVars(wiki)
        
        df = pd.concat([neuwal, wiki], axis=0)
        df.sort_values(by='Date', inplace=True)
        return df
        
         
    def _limit(self, input_df):
        df = input_df.copy()
        var = ['regionID', 'datum']
        df[var[0]] = pd.to_numeric(df[var[0]], downcast='integer')
        df = df[df[var[0]]==1]
        df[var[1]] = pd.to_datetime(df[var[1]])
        df = df[df[var[1]] > datetime(2016,12,1)]
        df = df[df[var[1]] > datetime(2016,12,1)]
        return df
    

    def _recode(self, input_df):
        df = input_df.copy()
        cols = [x for x in df.columns if re.search("Css", x)]
        for col in cols:
            parties = df[col].unique()
            for party in parties:
                if party not in df.columns:
                    df[party] = np.nan
                    
                df.loc[(df[col] == party), party] = df.loc[(df[col] == party), col[0:2]+"Value"]
        return df


    def _rename(self, input_df):
        df = input_df.copy()
        cols_dic = {
            "institut":"Institute",
            'datum':'Date',
            "ovp":"ÖVP",
            "spo":"SPÖ",
            "fpo":"FPÖ",
            "gru":"Grüne",
        }
        df = df[list(cols_dic.keys())]
        df = df.rename(columns=cols_dic)
        for var in ["ÖVP", "SPÖ", "FPÖ", "Grüne"]:
            df[var] = pd.to_numeric(df[var], downcast='integer')
        return df


    def _createVars(self, input_df):
        df = input_df.copy()
        # Binning of Data
        df["Treatment"] = np.where(df["Institute"].str.contains("Research Affairs"),1,0)
        df["Intervention"] = np.where(df["Date"] < datetime(2017,5,10), 0, 1)
        df["DiD"] = df["Treatment"] * df["Intervention"]
        df["bins"] = np.where(df.Date < datetime(2017,5,10), 1,
                               np.where(df.Date < datetime(2017,10,15),2,
                                    np.where(df.Date < datetime(2018,8,1),3,
                                            np.where(df.Date < datetime(2019,5,17),4,
                                                np.where(df.Date < datetime(2019,9,29),5,
                                                    np.where(df.Date < datetime(2020,3,16),6,
                                                             np.where(df.Date < datetime(2020,10,1),7,
                                                                      np.where(df.Date < datetime(2021,3,1),8,9))))))))
        return df
        
    
    def getMoneyData(self):
        path = self.path / "raw" / "money.csv"
        df = pd.read_csv(path)        
        keep = [x for x in df.columns if re.search("Betrag", x)]
        keep.append("Förderbetrag Gesamt")
        df.loc[14, keep] = df.loc[14, keep].str.replace(".",",")
        money = df.loc[14, keep].str.replace("€","\\euro").values
        df = pd.DataFrame(money,
                          columns=['Flow of Money'],
                          index=["2016", "2017", "2018", "2019", "2020", "overall"])
        print(df.style.to_latex(caption="Money Research Affairs was paid by the Austrian Ministry of Finance",
                                label="fig:Money",
                                position='h!'))


if __name__ == "__main__":
    handler = Handler('raw')
    df = handler.load(save=True)