
import pandas as pd
import numpy as np

class Preprocesser:
    """
    Preprocess Data for Analysis
    """
    
    def __init__(self, df):
        self.df = df
        

    def load(self):
        limit_cases(self.df)
        
        
    def new_vars(self, input_df):
        df = input_df.copy()
        
        
        df["inst_binary"] = np.where(df["Institute"] == "Research Affairs", 1, 0)
        return df
        
    def limit_cases(self, input_df):
        df = input_df.copy()
        var = "regionID"
        pd.to_numeric(df[var], downcast='integer')
        df = df[var==1]
        
        return df
        
    
    def define_columns(self, input_df):
        df = input_df.copy()
        
        # Drop Columns
        drop_list = []
        df = df.drop(columns={})
        
        # Rename Columns
        rename_dic = {
            
        }
        df = df.rename(columns=col_dic)
        
        return df
    
    
    def rearrange_voting_perc(self, input_df):
        df = input_df.copy()
        cols = [x for x in au_polls.columns if re.search("Css", x)]
        for col in cols:
            parties = df[col].unique()
            
            for party in parties:
                if party not in df.columns:
                    df[party] = np.nan
                    
                df.loc[(df[col] == party), party] = df.loc[(df[col] == party), col[0:2]+"Value"]
                
        return df
            
            
            
                
if __name__ == "__main__":
    preprocesser = Preprocesser()
    df = preprocesser.load()