
from cProfile import label
import logging
import re
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from datetime import datetime, timedelta


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
      
    def __init__(self):
        pass    
    

    def simData(self, T=9, noise=False, att=True, control=False):
        # Generate data with number of units = N, number of time = T
        N = 284
        T = T
        
        # Generate Variables
        D = np.random.randint(0,2,N)         # Treatment Indicator
        t = np.random.randint(1,T+1,N)       # Time Periods
        y1 = np.log(t+1)*15                  # Outcome 1
        y2 = ((1/t+1)*4)**1.5                  # Outcome 2
        
        # Create DataFrame abd adjust dtypes
        data = np.asmatrix([y1, y2, D, t])
        df = pd.DataFrame(data.T,
                          columns=['SPÖ', 'ÖVP', 'Treatment', 'bins']
        )
        df['Treatment'] = df.Treatment.astype(int)
        df['bins'] = df.bins.astype(int)
        df.sort_values(by='bins', inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # Define Treatment Effect 
        tau_övp = np.abs(np.random.randn(T)*2)
        tau_övp[0] = -2
        tau_övp[2] = 0
        tau_övp[3] = 0
        tau_spö = np.abs(np.random.randn(T)*2) * -1
        tau_spö[0] = 0.5
        tau_spö[2] = 0.5
        tau_spö[3] = 0.5

        if control:
            tau_övp[0] = 0
            tau_spö[0] = 0
        
        for idx in range(T): 
            df["ÖVP"] = np.where((df.bins==idx+1) & (df.Treatment==1), df.ÖVP+tau_övp[idx], df.ÖVP)    
            df["SPÖ"] = np.where((df.bins==idx+1) & (df.Treatment==1), df.SPÖ+tau_spö[idx], df.SPÖ)   
            
        # Possible Adjustments to outcome data
        if att:  # change baseline values of outcome variables
            df['ÖVP'] = np.where(df.Treatment==1, df.ÖVP+1.5, df.ÖVP)
            df['SPÖ'] = np.where(df.Treatment==1, df.SPÖ-1.5, df.SPÖ) 
        
        if noise: # Add random noise to the outcome data (e.g. sampling variance)
            df['ÖVP'] = np.random.normal(df.ÖVP,2)
            df['SPÖ'] = np.random.normal(df.SPÖ,2)

        self.tau = pd.DataFrame(data=[tau_övp.T, tau_spö.T],
                                index=['ÖVP', 'SPÖ'])
        self.data = df
        logging.info(f"Data created successfully!")

        
    def loadData(self, folder='analysis', save=False):
        path = pathlib.Path(__file__).parent.parent / 'data' / f'{folder}'
        
        if folder == 'raw':
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
        self.data = df
        logging.info(f"Data processed successfully!")

        
    def preprocess(self):
        neuwal = self.neuwal.copy()
        neuwal = self._limit(neuwal)
        neuwal = self._recode(neuwal)
        neuwal = self._rename(neuwal)
        missing = self._new_entries()
        neuwal = pd.concat([neuwal, missing])
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
        df = df[df[var[1]] != datetime(2019,5,20)]
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
            'datum':'Date',
            "institut":"Institute",
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
    
    
    def _new_entries(self):
        new = [
            # New Data based on Research Affairs archive
            [datetime(2018,7,12),"Research Affairs",33,26,24,5,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2018,7,26),"Research Affairs",33,27,24,4,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2018,11,19),"Research Affairs",34,25,24,6,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2018,12,13),"Research Affairs",34,25,24,6,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2019,1,13),"Research Affairs",34,26,24,5,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2019,1,24),"Research Affairs",34,26,23,6,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2019,2,21),"Research Affairs",34,25,24,6,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2019,4,18),"Research Affairs",34,24,23,5,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2019,5,2),"Research Affairs",34,25,22,5,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2019,8,8),"Research Affairs",36,22,20,10,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2019,8,14),"Research Affairs",35,21,19,11,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2019,8,22),"Research Affairs",35,21,19,11,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2019,8,29),"Research Affairs",36,22,20,11,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2019,9,5),"Research Affairs",36,22,20,11,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2019,9,12),"Research Affairs",35,22,19,11,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2019,9,19),"Research Affairs",34,23,10,12,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2019,9,21),"Research Affairs",34,23,21,11,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2020,2,27),"Research Affairs",39,17,11,17,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2020,3,26),"Research Affairs",40,18,11,18,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2020,10,8),"Research Affairs",41,19,11,12,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,1,14),"Research Affairs",39,24,16,9,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,2,5),"Research Affairs",39,24,15,9,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,2,25),"Research Affairs",37,24,17,9,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,3,11),"Research Affairs",37,23,16,9,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,6,10),"Research Affairs",35,23,14,12,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,6,17),"Research Affairs",35,22,15,12,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,6,24),"Research Affairs",34,23,16,11,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,7,15),"Research Affairs",35,20,18,11,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,7,22),"Research Affairs",35,20,18,12,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,8,5),"Research Affairs",35,21,19,10,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,8,12),"Research Affairs",34,21,19,11,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,8,19),"Research Affairs",34,21,18,10,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,8,26),"Research Affairs",34,21,17,11,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,9,8),"Research Affairs",35,22,18,11,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,9,16),"Research Affairs",35,23,18,10,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            [datetime(2021,9,23),"Research Affairs",35,24,17,10,600,"http://www.researchaffairs.at/Sonntagsfrage/"],
            # new data based on Strategieanalysen
            [datetime(2021,9,18),"Unique Research",35,21,19,12,800,"https://www.strategieanalysen.at/umfragen/polls.csv"],
            [datetime(2021,8,9),"Unique Research",35,21,19,12,800,"https://www.strategieanalysen.at/umfragen/polls.csv"],
            [datetime(2021,9,8),"Unique Research",35,21,19,12,800,"https://www.strategieanalysen.at/umfragen/polls.csv"],
            [datetime(2021,6,12),"Unique Research",33,23,18,13,800,"https://www.strategieanalysen.at/umfragen/polls.csv"],
            [datetime(2019,7,13),"Unique Research",35,20,21,11,800,"https://www.strategieanalysen.at/umfragen/polls.csv"],
            [datetime(2021,8,16),"Market",31,25,18,12,800,"https://www.strategieanalysen.at/umfragen/polls.csv"],
            [datetime(2021,7,15),"Market",33,25,17,12,800,"https://www.strategieanalysen.at/umfragen/polls.csv"],
            [datetime(2021,6,11),"Market",32,27,16,13,800,"https://www.strategieanalysen.at/umfragen/polls.csv"],
            [datetime(2021,6,27),"OGM",33,25,18,11,800,"https://www.strategieanalysen.at/umfragen/polls.csv"],
            [datetime(2019,1,21),"OGM",35,25,26,5,800,"https://www.strategieanalysen.at/umfragen/polls.csv"],
            [datetime(2021,6,25),"Peter Hajek",34,23,18,11,800,"https://www.strategieanalysen.at/umfragen/polls.csv"],
            [datetime(2021,7,26),"IFDD",35,22,19,11,800,"https://www.strategieanalysen.at/umfragen/polls.csv"],
            [datetime(2021,6,16),"IFDD",32,27,18,11,800,"https://www.strategieanalysen.at/umfragen/polls.csv"],

        ]
    
        df = pd.DataFrame(new,
                          columns=['Date', 'Institute', "ÖVP", "SPÖ", "FPÖ", "Grüne", "Sample Size", "url"])
        return df.iloc[:,:-2]


    def _createVars(self, input_df):
        df = input_df.copy()
        # Binning of Data for Analysis 
        # Alternatively pd.cut() function usable
        df["Treatment"] = np.where(df["Institute"].str.contains("Research Affairs"),1,0)        # Defining Treatment Assignment D = {0,1}
        df["bins"] = np.where(df.Date < datetime(2017,5,10), 1,                                 # Define Binning of Data into T=9 timepoints 
                               np.where(df.Date < datetime(2017,10,15),2,
                                    np.where(df.Date < datetime(2018,8,1),3,
                                            np.where(df.Date < datetime(2019,5,17),4,
                                                np.where(df.Date < datetime(2019,9,29),5,
                                                    np.where(df.Date < datetime(2020,3,16),6,
                                                             np.where(df.Date < datetime(2020,11,1),7,
                                                                      np.where(df.Date < datetime(2021,4,1),8,9))))))))
        return df


    def getMoneyData(self):
        """
        Function for replicating Table of money flow in thesis.
        """
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


    def scatter(self, var='ÖVP', binning=False, save=False, missing=True):
        if isinstance(self.data, pd.DataFrame):
            df = self.data.copy()
            
            if 'Date' in df.columns:   
                with plt.style.context('ggplot'):
                    fig, ax = plt.subplots(figsize=(14,5))
                    ax.scatter("Date", var, data=df[df["Treatment"]==1], 
                            label="Research Affairs", 
                            s=15,
                            c='gray',
                            
                    )
                    ax.scatter("Date", var, data=df[df["Treatment"]==0], 
                            label="Other Institutes",
                            s=15,
                            c='white',
                            alpha=.6,
                            edgecolors='black'
                    )
                    ax.legend(fancybox=True)
                    if missing:
                        mis = pd.DataFrame([[datetime(2019,5,20), 38,26,18,5]],
                                          columns=['Date', 'ÖVP', "SPÖ", "FPÖ", "Grüne"])
                        ax.scatter("Date", var, data=mis,
                                   s=15,
                                   c='red',
                                   alpha=.5,
                        )
                    if binning:
                        # Create Lines seperating bins
                        upper = df.groupby('bins')['Date'].max()[:-1].reset_index(drop=True)
                        lower = df.groupby('bins')['Date'].min()[1:].reset_index(drop=True)
                        bins = lower + (upper - lower)/2              
                        ax.vlines(bins, 
                                  ymin=df[var].min()-1, 
                                  ymax=df[var].max()+1, 
                                  color='gray',
                                  lw=.6,
                                  alpha=.6, 
                                  ls='--')
                        # Plotting mean value of each bin with fixed distances
                        pos = []
                        pos.append(df.Date.min()-timedelta(5))
                        pos[1:len(bins)] = bins
                        pos.append(df.Date.max()+timedelta(5))
                        for b in df.bins.unique():
                            ax.hlines(df.loc[(df.bins==b) & (df.Treatment==1), var].mean(),
                                    xmin=pos[b-1]+timedelta(15),
                                    xmax=pos[b]-timedelta(15),
                                    color="gray",
                                    lw=.5
                            )
                            ax.hlines(df.loc[(df.bins==b) & (df.Treatment==0), var].mean(),
                                    xmin=pos[b-1]+timedelta(15),
                                    xmax=pos[b]-timedelta(15),
                                    color='black',
                                    lw=.5
                            )
                    ax.set_xlim([df.Date.min()-timedelta(20), df.Date.max()+timedelta(20)])
                    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
                    ax.xaxis.set_minor_locator(mdates.MonthLocator())
                    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
                    ax.set_ylim(df[var].min()-2, df[var].max()+2)    
                    ax.set_ylabel("Estimated Vote Share")
                    if save == True:
                        path = pathlib.Path(__file__).parent.parent / 'images' / f'scatter{var}.pdf'
                        plt.savefig(path, dpi=800, format='pdf')
                    else:
                        plt.show()
                    
            else:
                print('No data with continous x-range loaded yet! Use .loadData() to get DataFrame for plotting!')
        else:
            print('No data loaded yet! Use .simData() or .loadData() to get DataFrame for plotting!')
    
    
    def trends(self, var=None, diff=.1):   
        if isinstance(self.data, pd.DataFrame):         
            df = self.data.copy() 
            with plt.style.context('ggplot'):  
                if var:
                    _, ax = plt.subplots(figsize=(10,5))
                    tg = df[df.Treatment==1].groupby('bins')[var].mean().values   
                    cg = df[df.Treatment==0].groupby('bins')[var].mean().values   
                    ax.errorbar(df.bins.unique()+diff,
                                tg, 
                                df[df.Treatment==1].groupby('bins')[var].std().values,
                                elinewidth=.7,
                                color='gray',
                                fmt='o',
                                capsize=4,
                                label='Research Affairs'
                    )
                    ax.errorbar(df.bins.unique()-diff,
                                cg, 
                                df[df.Treatment==0].groupby('bins')[var].std().values,
                                elinewidth=.5,
                                fmt='ok',
                                capsize=4,
                                markerfacecolor="white",
                                label='Other Institutes'
                    )
                    ax.legend(fancybox=True)
                    ax.set_ylabel(f"Estimated Voting % for {var}")
                    ax.set_title("Mean and Standard Deviation of time points")
                else:
                    fig, ax = plt.subplots(1,2,figsize=(15,5), sharex=True, sharey=True, constrained_layout=True)
                    for axs, var in enumerate(['ÖVP', 'SPÖ']):
                        ax[axs].errorbar(df.bins.unique()+diff,
                                    df[df.Treatment==1].groupby('bins')[var].mean().values, 
                                    df[df.Treatment==1].groupby('bins')[var].std().values,
                                    elinewidth=.7,
                                    color='gray',
                                    fmt='o',
                                    capsize=4,
                                    label='Research Affairs'
                        )
                        ax[axs].errorbar(df.bins.unique()-diff,
                                    df[df.Treatment==0].groupby('bins')[var].mean().values, 
                                    df[df.Treatment==0].groupby('bins')[var].std().values,
                                    elinewidth=.5,
                                    fmt='ok',
                                    capsize=4,
                                    markerfacecolor="white",
                                    label='Other Institutes'
                        )
                        ax[axs].set_title(f"{var}",fontsize=13)
                        ax[axs].set_title(f'{var}',fontsize=13)    
                    fig.suptitle('Binned Differences for major parties in Austria with means and standard deviations', fontsize=16)
                    fig.supxlabel('Time')
                    fig.supylabel('Estimated Voting %')
                plt.legend(fancybox=True)
                plt.xticks(df.bins.unique()) 
                plt.show()    
        else:
            print('No data loaded yet! Use .simData() or .loadData() to get DataFrame for plotting!')

    
    def hist(self):
        df = self.data.copy()
        if 'Date' in df.columns:   
            df['Treatment'] = np.where(df.Institute.str.contains('Unique Research'),2,df.Treatment)
        with plt.style.context('seaborn-darkgrid'):
            _,ax = plt.subplots(figsize=(20,5), tight_layout=True)
            pd.crosstab(df['bins'], df['Treatment']).plot.bar(ax=ax,
                                                            color=['olive', 'darkgrey', 'orange'],
                                                            alpha=.6)
            ax.set_xticks(df.bins.unique()-1)
            label = []
            for i in range(len(df.bins.unique())):
                label.append(f'Group {i}')
            ax.set_xticklabels(label)
            ax.tick_params(axis="x", rotation=360)
            ax.legend(['Other Institutes', 'Research Affairs', 'Unique Research'])

    
if __name__ == "__main__":
    handler = Handler()
    handler.loadData(folder='raw')