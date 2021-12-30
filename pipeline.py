# %% SetUp Logging
import logging

logging.basicConfig(
    format="%(levelname)s\t %(asctime)s\t %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO, # change to logging.ERROR to only log errors
)
# %%   # ------------------------- imports ------------------------- #
from scripts.config import Configurator
from scripts.data_scraper import Scraper
from scripts.data_preprocesser import Preprocesser
from scripts.data_handler import Handler
# %%   # ------------------------ init objs ------------------------ #
configurator = Configurator()
scraper = Scraper()
preprocesser = Preprocesser()
handler = Handler()
# %%   # ------------------------ run pipeine ------------------------ #
def run_pipeline():
    scraper.update()        
    polls = scraper.load()
    preprocesser.update(polls)
    """What to do with ambigious data 
    -> Take mean and safe intervals 
    """
    
    au_polls = preprocesser.load()
    handler.update(au_polls)
    handler.plotDifference("SPÖ")
    handler.diff_in_diff("SPÖ")


if __name__== "__main__":
    run_pipeline()