
import logging
import json
import requests
import lxml
import pandas as pd
from requests.models import Response
from tqdm import tqdm
from bs4 import BeautifulSoup

class Scraper:
    """
    scrape wahl
    """
    
    def __init__(self, url="wiki"):
        
        if url == "wiki":
            self.url = "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2017_Austrian_legislative_election"
        elif url == "neuwal":
            self.url = "https://neuwal.com/wahlumfragen/data/neuwal-wahlumfragen-user.json"
        elif url == "polyd":
            self.url = "https://de.polyd.org/get/polls/AT-parliament/format/csv"
        elif url == "strategie":
            self.url = "https://www.strategieanalysen.at/umfragen/polls.csv"
        else:
            print("Invalid URL specification!")
        
        
    def update(self, url):
        self.url = url
        
     
    def load(self):
        if "neuwal" in self.url:
            logging.info("Loading data...")
            try:
                response = requests.get(self.url)
            except Exception as err:
                logging.error(f"Error while trying to read data: {err}")
                return False
            if response.status_code == 200:
                logging.info(f"Status OK")
                dictionary = json.loads(response.text)["data"]                
                df = pd.DataFrame(dictionary)
                logging.info(f"Data loaded")
            else:
                logging.error(f'Something went wrong: {response.status_code}')
                return None
        
        elif "wiki" in self.url:
            soup = self.load_soup()
            if soup:
                table_div = soup.find("table")
                df = self.parse(table_div)
            return soup
        
        elif "strategie" or "polyd" in self.url:
            logging.info("Loading data...")
            try:
                response = requests.get(self.url)
            except Exception as err:
                logging.error(f"Error while trying to read data: {err}")
                return False
            if response.status_code == 200:
                df = pd.read_csv(self.url)
                logging.info(f"Data loaded")
            else:
                logging.error(f'Something went wrong: {response.status_code}')
                return None
        
        return df, self.url
    
    def load_soup(self):
        logging.info("Loading data...")
        try:
            response = requests.get(self.url)
        except Exception as err:
            logging.error(f"Error while trying to read data: {err}")
            return False
        if response.status_code == 200:
            logging.info(f"Status OK")
            soup = BeautifulSoup(response.content, "lxml")
            logging.info(f"Soup loaded")
            return soup
        else:
            logging.error(f'Something went wrong: {response.status_code}')
            return False


    def parse(self, table_div):
        header = [x for x in [*map(lambda x: x.replace("\n", ""), [h.get_text() for h in table_div.find_all("th")])] if x]
        body = table_div.find("tbody")
        raw_rows = body.find_all("tr")
        raw_rows = raw_rows[2:]        
        rows = []
        for r_row in raw_rows:            
            row_els = r_row.find_all("td")
            if len(row_els) < 5:
                continue
            # get text of cells
            r = [x.get_text() for x in row_els]
            r = [*map(lambda x: x.replace("\n", ""), r)]

            if row_els[0].has_attr("rowspan"):
                self.last_poll_firm = r[0]
                self.last_poll_date = r[1]            
            rows.append(r)
            
        df = pd.DataFrame(rows)
        df.columns = header
        
        return df
    
        
if __name__ == "__main__":
    scraper = Scraper()
    df = scraper.load()