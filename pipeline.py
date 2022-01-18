"""
Since Intervention Time seems to become a relevant factor, I should
create a binary variable to distinguish between dates
and also datasets for the future.
after Kurz becomes leader
before Kurz announces ambition
"""



# SetUp Logging
import logging

logging.basicConfig(
    format="%(levelname)s\t %(asctime)s\t %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO, # change to logging.ERROR to only log errors
)
# -------------------------- imports -------------------------- #
from scripts.data_scraper import Scraper
from scripts.data_preprocessor import Preprocessor
from scripts.data_handler import Handler
# ------------------------- init objs ------------------------- #
scraper = Scraper()
preprocessor = Preprocessor()
handler = Handler()
# ------------------------ run pipeine ------------------------ #
def run_pipeline():
    polls, url = scraper.load()
    preprocessor.update(polls, url)
    au_polls = preprocessor.load()
    handler.update(au_polls, var="ÖVP")
    handler.plotData()
    handler.diff_in_diff()


if __name__== "__main__":
    run_pipeline()