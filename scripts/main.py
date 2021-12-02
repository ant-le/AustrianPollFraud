#%%
import datetime
import pandas as pd
import numpy as np
import re
from data_scraper import Scraper
#from data_preprocesser import Data_Processer
# %% Scripe Data from Source
scraper = Scraper()
dic, df = scraper.load()
polls = df.copy(deep=True)
#%% Change dtypes of Columns
polls["regionID"] = pd.to_numeric(polls["regionID"], downcast='integer')
polls["datum"] = pd.to_datetime(polls["datum"])

cols = [x for x in polls.columns if re.search("Value",x)]
polls[cols] = polls[cols].apply(pd.to_numeric)
# %% Limit Cases to Surveys about National Parties
mask = polls["regionID"] == 1
au_polls = polls[mask]
au_polls = au_polls.drop(columns={"regionID", "region", "id", "medium"})
# %% Rearrange ÖVP vote shares
def rearrange_voting_perc(input_df):
    df = input_df.copy()
    cols = [x for x in au_polls.columns if re.search("Css", x)]
    for col in cols:
        parties = df[col].unique()
        
        for party in parties:
            if party not in df.columns:
                df[party] = np.nan
                
            df.loc[(df[col] == party), party] = df.loc[(df[col] == party), col[0:2]+"Value"]
            
            
    drop_cols = [x for x in au_polls.columns if re.search("(Party|Css|Value)", x)]
    df = df.drop(columns={drop_cols})      
                                  
    return df

au_polls = rearrange_voting_perc(au_polls)
#%%
cols = [x for x in au_polls.columns if re.search("(Party|Css|Value)", x)]
cols
# %%
au_polls
# %%
