
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
from scripts.data_preprocessor import Preprocessor
from model.differences import Diff_in_Diff_Model
# ------------------------- init objs ------------------------- #
configurator = Configurator()
scraper = Scraper(config=configurator)
preprocessor = Preprocessor(config=configurator)
model1 = Diff_in_Diff_Model()
# ------------------------ run pipeline ------------------------ #
def run_pipeline():
    polls = scraper.load()
    preprocessor.update(polls)
    au_polls = preprocessor.load()
    model1.fitData(au_polls["polyd"])
    model1.ols_regression()
    model1.summary()

if __name__== "__main__":
    run_pipeline()