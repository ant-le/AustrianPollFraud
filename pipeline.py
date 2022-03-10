
# SetUp Logging
import logging
logging.basicConfig(
    format="%(levelname)s\t %(asctime)s\t %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO, # change to logging.ERROR to only log errors
)
# -------------------------- imports -------------------------- #
from scripts.scraper import Scraper
from scripts.handler import Handler
from scripts.plotter import Plotter
from model.bayesian_regression import BayesRegression
# ------------------------- init objs ------------------------- #
# scraper = Scraper()
handler = Handler()
plotter = Plotter()
# model = BayesRegression()
# ------------------------ run pipeline ------------------------ #
def run_pipeline():
    polls = handler.load()
    plotter.scatter(polls)
    plotter.trends(polls, error=True)
    # model.sample(polls)
    # model.summary()
    
    
if __name__== "__main__":
    run_pipeline()