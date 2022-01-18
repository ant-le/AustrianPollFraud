
from scripts.data_scraper import Scraper
from scripts.data_preprocesser import Preprocesser

def compareData():
    scraper = Scraper()
    preprocesser = Preprocesser()
    
    dfs = ["polyd", "wiki", "strategie", "neuwal"]
    for df in dfs:
        polls, url = scraper.load(url=df)
        preprocesser.update(polls, url)
        df = preprocesser.load()
        keep = ["Institute", "Date", "ÖVP", "SPÖ", "FPÖ", "Grüne"]
        df = df[keep]
    

if __name__== "__main__":
    pass