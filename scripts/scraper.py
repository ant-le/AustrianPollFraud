
import logging
import requests
import pandas as pd
from pathlib import Path

class Scraper:
    """
    Class which includes all relevant functionalities to automatically scrape the necessary 
    data from various sources. Depending on the specification in the Configurator()-Class either
    all datasets will be scraped or only the specified one.
    """
    
    def __init__(self):
        self.url = 'https://de.polyd.org/get/polls/AT-parliament/format/csv'
        
        
    def load(self, save=False):
        try:
            response = requests.get(self.url)
        except Exception as err:
            logging.error(f"Error while trying to read data: {err}")
            return False
        if response.status_code == 200:
            df = pd.read_csv(self.url)
            if save:
                path = Path(__file__).parent.parent / "data" / "raw" / "polls.csv"
                df.to_csv(path, index=False)  
                logging.info("Data loaded successfully!")
          
            return df
        else:
            logging.error(f'Something went wrong: {response.status_code}')
            return None


if __name__ == "__main__":
    scraper = Scraper()
    df = scraper.load()