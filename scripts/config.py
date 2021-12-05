
from pathlib import Path

class Directory:
    
    def __init__(self):
        self.path = Path(__file__).parent.parent

    
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