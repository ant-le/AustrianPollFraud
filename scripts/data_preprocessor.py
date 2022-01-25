
import logging
from pickletools import read_uint1
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.api.types import is_string_dtype
import seaborn as sns
import numpy as np
import pathlib
import datetime as dt

from scripts.config import Configurator

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
      
    def __init__(self, config, df=None, date=dt.datetime(2017,10,15)):
        self.df = df
        self.date = date
        self.config = config
               
               
    def update(self, df=None, url=None, date=None):
        if df:
            self.df = df
        if url:
            self.config.url = url
        if date:
            self.date = date
        

    def load(self, save=False):
        if self.config.type is "scrape" or self.config.type is "raw":
            if self.config.type is "raw":
                self._getData()
                logging.info("Data loaded successfully!")
                
            if self.df is not None:
                self.df['wiki'] = self._processwiki()
                self.df['neuwal'] = self._processneuwal()
                self.df['polyd'] = self._processpolyd()
                self.df['strategie'] = self._processstrategie()
                logging.info(f"Data preprocessed successfully!")

                if save:
                    for df in self.df.keys():
                        if self.df[df] is not None:
                            self.config.writeAnalysisData(self.df[df], name=df, overwrite=True)                    
            else:
                print("There must be a dataset given for preprocessing!")
        
        else:
            self._getData()
            logging.info("Data loaded successfully!")
            
        return self.df


    def _processwiki(self):
        if 'wiki' in self.config.url or 'all' in self.config.url:
            df = self.df['wiki'].copy()
            
            df = df.drop(df.index[0])
            
            df = df[df["ÖVP"].str.isdigit()]  
            df["Grüne"] = df["Grüne"].str.strip("[b]")
            
            cols_dic = {
                "ÖVP":"ÖVP",
                "SPÖ":"SPÖ",
                "FPÖ":"FPÖ",
                "Grüne":"Grüne",
                "Polling firm": "Institute",
                "End date": "Date",
            }
            df = self._definecolumns(df, cols_dic)
            df = self._analysisVars(df)
            return df


    def _processneuwal(self):
        if 'neuwal' in self.config.url or 'all' in self.config.url:
            # Limit cases
            df = self.df['neuwal'].copy()
            df.rename(columns={'datum':'date'}, inplace=True)

            df['regionID'] = pd.to_numeric(df['regionID'], downcast='integer')
            df = df[df['regionID'] == 1]
            df = self._limitdate(df)
            
            # Recode Voting Percentages
            cols = [x for x in df.columns if re.search("Css", x)]
            for col in cols:
                parties = df[col].unique()
                for party in parties:
                    if party not in df.columns:
                        df[party] = np.nan       
                    df.loc[(df[col] == party), party] = df.loc[(df[col] == party), col[0:2]+"Value"]

            cols_dic = {
                "ovp":"ÖVP",
                "spo":"SPÖ",
                "fpo":"FPÖ",
                "gru":"Grüne",
                "institut":"Institute",
                "date":"Date",
                "n":"Sample Size"
            }
            df = self._definecolumns(df, cols_dic)
            df = self._analysisVars(df)
            return df

    
    def _processpolyd(self):
        if 'polyd' in self.config.url or 'all' in self.config.url:
            df = self.df['polyd'].copy()
            df = self._limitdate(df)
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
            df = self._definecolumns(df, cols_dic)
            df = self._analysisVars(df)            
            return df
    
    
    def _processstrategie(self):
        if 'strategie' in self.config.url or 'all' in self.config.url:
            df = self.df['strategie'].copy()
            df = self._limitdate(df)
            cols_dic = {
                "oevp":"ÖVP",
                "spoe":"SPÖ",
                "fpoe":"FPÖ",
                "gruene":"Grüne",
                "institute":"Institute",
                "date":"Date",
                "sample":"Sample Size"
            }
            df = self._definecolumns(df, cols_dic)
            df = self._analysisVars(df)
            return df
    

    def _limitdate(self, df):
        df['date'] = pd.to_datetime(df['date'])
        df = df[df['date'].dt.year == 2017]
        df = df[df['date'] < self.date]
        return df
            

    def _definecolumns(self, inputdf, dic):
        df = inputdf.copy()
        
        df = df[list(dic.keys())]
        df = df.rename(columns=dic)
                
        # Changing dtype of column
        keep = ["ÖVP", "SPÖ", "FPÖ", "Grüne"]
        if "Sample Size" in df.columns:
            keep.append("Sample Size")
        if "Sampling Variance" in df.columns:
            keep.append("Sampling Variance")
        
        
        for var in keep:
            if is_string_dtype(df[var]):
                df[var] = df[var].str.replace(",", ".")
                df[var] = pd.to_numeric(df[var])
        
        df["Date"] = pd.to_datetime(df["Date"])

        return df


    def _analysisVars(self, inputdf):
        df = inputdf.copy()
         # Recode institute to binary var
        df["Treatment"] = np.where(df["Institute"].str.contains("Research Affairs"),1,0)
        df.sort_values(by=['Date'], inplace=True)

        return df


    def _getData(self):
        self.df = {}
        dfs = []
        if self.config.url is "all":
            dfs.extend(["wiki", "neuwal", "polyd", "strategie"])
        else:
            dfs.append(self.config.url)
                
        for df in dfs:
            if self.config.type is "processed":
                self.df[df] = self.config.getAnalysisData(name=df)
                self.df[df]["Date"] = pd.to_datetime(self.df[df]["Date"])  
            else:
                self.df[df] = self.config.getRawData(name=df)
                

    def descriptivePlot(self, var="ÖVP", save=False, intervention=dt.datetime(2017,5,10), url="polyd"):
        if self.config.url is not "all":
            url2 = self.config.url
        else:
            url2 = url
        if self.df:
            df = self.df[url2]
            months = df.Date.dt.strftime("%b").unique()
            with plt.style.context('bmh'):
                fig, ax = plt.subplots(figsize=(10,5))
                ax.scatter("Date", var, data=df[df["Treatment"]==1], 
                           label="Research Affairs", c='sandybrown', s=25)
                ax.scatter("Date", var, data=df[df["Treatment"]==0], 
                           label="Other Institutes", c='royalblue', s=25)
                ax.axvline(intervention, c='lightgrey', ls="--", label="Leadership Change")
                ax.legend(fancybox=True)
                ax.set(xticklabels=months)  
                ax.set(xlabel="Date")
                ax.set(ylabel="Estimated Voting % or " + str(var))
                ax.tick_params(bottom=False)
                plt.show()
                
                if save is True:
                    configurator = Configurator()
                    path = configurator.imageFolder().joinpath(str(var) + "_difference.jpg")
                    fig.savefig(path, dpi=300)
                

if __name__ == "__main__":
    pass