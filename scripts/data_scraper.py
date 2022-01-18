
import logging
import json
import re
import requests
import lxml
import pandas as pd
from requests.models import Response
from tqdm import tqdm
from bs4 import BeautifulSoup

from scripts.config import Configurator

class Scraper:
    """
    scrape wahl
    """
    
    def __init__(self, url="all"):
        self.url = url
        self.configurator = Configurator()
                
        
    def update(self, url):
        self.url = url
        
        
    def load(self):
        df_wiki = self._loadwiki()
        df_neuwal = self._loadneuwal()
        df_strategie = self._loadstrategie()
        df_polyd = self._loadpolyd()
        
        if "all" in self.url:
            keys = ["wiki", "neuwal", "strategie", "polyd"]
        else:
            keys = [self.url]
            
        values = [x for x in [df_wiki, df_neuwal, df_strategie, df_polyd] if x is not None]
        dfs = dict(zip(keys, values))
        return dfs, self.url     


    def _loadneuwal(self):
        if 'all' in self.url or 'neuwal' in self.url:
            #logging.info("Loading data...")
            try:
                response = requests.get('https://neuwal.com/wahlumfragen/data/neuwal-wahlumfragen-user.json')
            except Exception as err:
                logging.error(f"Error while trying to read data: {err}")
                return False
            if response.status_code == 200:
                dictionary = json.loads(response.text)["data"]                
                df = pd.DataFrame(dictionary)
                logging.info(f"Neuwal Data loaded")
                return df
            else:
                logging.error(f'Something went wrong: {response.status_code}')
                return None
        else:
            return None
     
     
    def _loadpolyd(self):
        if 'all' in self.url or 'polyd' in self.url:
            #logging.info("Loading data...")
            try:
                response = requests.get('https://de.polyd.org/get/polls/AT-parliament/format/csv')
            except Exception as err:
                logging.error(f"Error while trying to read data: {err}")
                return False
            if response.status_code == 200:
                df = pd.read_csv('https://de.polyd.org/get/polls/AT-parliament/format/csv')
                logging.info(f"Polyd Data loaded")
                return df
            else:
                logging.error(f'Something went wrong: {response.status_code}')
                return None
        else:
            return None
    
    
    def _loadstrategie(self):
        if 'all' in self.url or 'strategie' in self.url:
            #logging.info("Loading data...")
            try:
                response = requests.get('https://www.strategieanalysen.at/umfragen/polls.csv')
            except Exception as err:
                logging.error(f"Error while trying to read data: {err}")
                return False
            if response.status_code == 200:
                df = pd.read_csv('https://www.strategieanalysen.at/umfragen/polls.csv')
                logging.info(f"Strategie Data loaded")
                return df
            else:
                logging.error(f'Something went wrong: {response.status_code}')
                return None
        else:
            return None
    

    def _loadwiki(self):
        if 'all' in self.url or 'wiki' in self.url:
            try:
                response = requests.get('https://en.wikipedia.org/wiki/Opinion_polling_for_the_2017_Austrian_legislative_election')
            except Exception as err:
                logging.error(f"Error while trying to read data: {err}")
                return False
            if response.status_code == 200:
                #logging.info(f"Status OK")
                soup = BeautifulSoup(response.content, "lxml")
                #logging.info(f"Soup loaded")
                if soup:
                    table_div = soup.find("table")
                    df = self.parse(table_div)
                    logging.info(f"Wiki Data loaded")
                return df
            else:
                logging.error(f'Something went wrong: {response.status_code}')
                return False
        else:
            return None
                
    
    def parse(self, table_div):
        header = [x for x in [*map(lambda x: x.replace("\n", ""), [h.get_text() for h in table_div.find_all("th")])] if x]
        body = table_div.find("tbody")
        raw_rows = body.find_all("tr")
        raw_rows = raw_rows[2:]        
        rows = []
        rowspan = False
        last_poll_firm = ""
        last_poll_date = ""
        
        for r_row in raw_rows:            
            row_els = r_row.find_all("td")
            if len(row_els) < 5:
                continue
            # get text of cells
            r = [x.get_text() for x in row_els]
            r = [*map(lambda x: x.replace("\n", ""), r)]
            
            if rowspan:
                r = [last_poll_firm, last_poll_date] + r
                rowspan = False
                
            if row_els[0].has_attr("rowspan"):
                rowspan = True
                last_poll_firm = r[0]
                last_poll_date = r[1]            
            rows.append(r)
            
        df = pd.DataFrame(rows)
        df.columns = header
        
        return df
    
        
if __name__ == "__main__":
    scraper = Scraper()
    dfs = scraper.load()
    
