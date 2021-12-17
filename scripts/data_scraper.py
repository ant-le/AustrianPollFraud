
import logging
import json
import requests
import pandas as pd
from requests.models import Response
from tqdm import tqdm

class Scraper:
    """
    scrape wahl
    """
    
    def __init__(self):
        self.wiki = "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2017_Austrian_legislative_election"
        self.neuwal = "https://neuwal.com/wahlumfragen/data/neuwal-wahlumfragen-user.json"
        self.strategie = "https://www.strategieanalysen.at/umfragen/polls.csv"
    
    def load(self):
        logging.info("Loading data...")
        try:
            response = requests.get(self.neuwal)
        except Exception as err:
            logging.error(f"Error while trying to read data: {err}")
            return False
        if response.status_code == 200:
            logging.info(f"Status OK")
            dictionary = json.loads(response.text)["data"]                
            df = pd.DataFrame(dictionary)
            logging.info(f"Data loaded")
            return df
        else:
            logging.error(f'Something went wrong: {response.status_code}')
            return None
            

    def load2(self):
        logging.info("Loading data...")
        try:
            response = requests.get(self.strategie)
        except Exception as err:
            logging.error(f"Error while trying to read data: {err}")
            return False
        if response.status_code == 200:
            logging.info(f"Status OK")
            df = pd.read_csv(self.strategie)
            logging.info(f"Data loaded")
            return df
        else:
            logging.error(f'Something went wrong: {response.status_code}')
            return None


    def loadwiki(self):
        logging.info("Loadding data...")
        try:
            response = requests.get(self.wiki)
        except Exception as err:
            logging.error(f"Error while trying to read data: {err}")
            return False
        if response.status_code == 200:
            logging.info(f"Status OK")
        
        
        
        
if __name__ == "__main__":
    scraper = Scraper()
    dictionary, df = scraper.load()