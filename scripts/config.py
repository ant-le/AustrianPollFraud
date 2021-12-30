
from pathlib import Path
import pandas as pd

class Configurator:
    
    def __init__(self):
        self.path = Path(__file__).parent.parent
        
        
    def getRawData(self):
        df = pd.read_csv(self.rawFolder() / "polls.csv")
        return df

    def getAnalysisData(self):
        df = pd.read_csv(self.analysisFolder() / "au_polls.csv")
        return df
    
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