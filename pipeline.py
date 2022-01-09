# %%
# SetUp Logging
import logging

logging.basicConfig(
    format="%(levelname)s\t %(asctime)s\t %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO, # change to logging.ERROR to only log errors
)
# -------------------------- imports -------------------------- #
from scripts.config import Configurator
from scripts.data_scraper import Scraper
from scripts.data_preprocesser import Preprocesser
from scripts.data_handler import Handler
# ------------------------- init objs ------------------------- #
configurator = Configurator()
scraper = Scraper()
preprocesser = Preprocesser()
handler = Handler()
# ------------------------ run pipeine ------------------------ #
def run_pipeline():
    polls, url = scraper.load()
    preprocesser.update(polls, url)
    au_polls = preprocesser.load()
    handler.update(au_polls)
    handler.plotData()
    handler.diff_in_diff()


if __name__== "__main__":
    run_pipeline()