
from pathlib import Path
import pandas as pd

class Configurator:
    
    def __init__(self):
        self.path = Path(__file__).parent.parent
        
        
    def getRawData(self, name="polls"):
        df = pd.read_csv(self.rawFolder().joinpath(name + ".csv"))
        return df


    def getAnalysisData(self, name="au_polls"):
        df = pd.read_csv(self.analysisFolder().joinpath(name + ".csv"))
        return df
    
    
    def writeRawData(self, df, name="polls", overwrite=False):
        path = self.path.rawFolder().joinpath(name + ".csv")
        if path.exists():
            if overwrite is True:
                df.to_csv(path, index=False)
            else:
                print("Filename already exists!")
        else:
            df.to_csv(path, index=False)
            
            
    def writeAnalysisData(self, df, name="au_polls", overwrite=False):
        path = self.path.analysisFolder().joinpath(name + ".csv")
        if path.exists():
            if overwrite is True:
                df.to_csv(path, index=False)
            else:
                print("Filename already exists!")
        else:
            df.to_csv(path, index=False)
    
    
    def analysisFolder(self):
        return self.path / "data" / "analysis"
    
    
    def rawFolder(self):
        return self.path / "data" / "raw"
    
    
    def replicationFolder(self):
        return self.path / "data" / "replication"
    
    
    def imageFolder(self):
        return self.path / "images"
    

if __name__ == "__main__":
    pass