
# SetUp Logging
import logging
from re import S
logging.basicConfig(
    format="%(levelname)s\t %(asctime)s\t %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO, # change to logging.ERROR to only log errors
)
# -------------------------- imports -------------------------- #
from scripts.scraper import Scraper
from scripts.handler import Handler
from model.bayesian_regression import BayesRegression
# ------------------------- init objs ------------------------- #
scraper = Scraper()
handler = Handler()
ovp = BayesRegression()
spo = BayesRegression('SPÖ')
# ------------------------ run pipeline ------------------------ #
def run_pipeline():
    handler.loadData()
    spo.sample(handler.data)
    ovp.sample(handler.data)
     
if __name__== "__main__":
    run_pipeline()