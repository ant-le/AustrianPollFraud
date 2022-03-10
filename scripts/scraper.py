
import json
import lxml
import re
import logging
import requests
import pathlib
import pandas as pd
from bs4 import BeautifulSoup

class Scraper:
    """
    Class which includes all relevant functionalities to automatically scrape the necessary 
    data from various sources. Depending on the specification in the Configurator()-Class either
    all datasets will be scraped or only the specified one.
    """

 
    def __init__(self):
        self.neuwal = "https://neuwal.com/wahlumfragen/data/neuwal-wahlumfragen-user.json"
        self.wiki = "https://de.wikipedia.org/wiki/28._Nationalratswahl_in_Österreich/Umfragen_und_Prognosen"


    def load(self, save=False):
        neuwal = self._loadNeuwal()
        wiki = self._loadWiki()
        if save:
            path = pathlib.Path(__file__).parent.parent / "data" / "raw"
            wiki.to_csv(path.joinpath("wiki.csv"), index=False)
            neuwal.to_csv(path.joinpath("neuwal.csv"), index=False)

        return wiki, neuwal
    
    
    def _loadNeuwal(self):
        try:
            response = requests.get(self.neuwal)
        except Exception as err:
            logging.error(f"Error while trying to read data: {err}")
            return False
        if response.status_code == 200:
            logging.info(f"Status OK")
            dictionary = json.loads(response.text)["data"]
            df = pd.DataFrame(dictionary)
            logging.info(f"Data loaded successfully")
            return df
        else:
            logging.error(f'Something went wrong: {response.status_code}')


    def _loadWiki(self):
        try:
            response = requests.get(self.wiki)
        except Exception as err:
            logging.error(f"Error while trying to read data: {err}")
            return False
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "lxml")
            rows = []
            
            for i in range(1,3):  
                tbl = soup.find_all("table",{"class":"wikitable sortable zebra center"})[i]
                if i == 1:
                    header = [x for x in [*map(lambda x: x.replace("\n", ""), [h.get_text() for h in tbl.find_all("th")])] if x]
                    rows.append(header[0:6])
                body = tbl.find_all(['tr'])[1:-1]
                for row in body:
                    cont = row.find_all("td")
                    r = [x.get_text() for x in cont]
                    r = [*map(lambda x: x.replace("\n", ""), r)]
                    r = [*map(lambda x: x.replace("\xa0%", ""), r)]
                    r = [(re.sub(r'\[.+?\]\s*', "", x)) for x in r]
                    rows.append(r[0:6])
                    
            df = pd.DataFrame(rows[1:], columns=rows[0])
            return df
    
        else:
            logging.error(f'Something went wrong: {response.status_code}')
            return False


if __name__ == "__main__":
    scraper = Scraper()
    df = scraper.load(save=True)