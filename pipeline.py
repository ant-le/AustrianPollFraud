
# SetUp Logging
import logging

from matplotlib.pyplot import plot

logging.basicConfig(
    format="%(levelname)s\t %(asctime)s\t %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO, # change to logging.ERROR to only log errors
)
# -------------------------- imports -------------------------- #
from scripts.scraper import Scraper
from scripts.preprocessor import Preprocessor
from scripts.plotter import Plotter
from model.diff_in_diff import Diff_in_Diff_Regression
# ------------------------- init objs ------------------------- #
scraper = Scraper()
preprocessor = Preprocessor()
plotter = Plotter()
model1 = Diff_in_Diff_Regression()
# ------------------------ run pipeline ------------------------ #
def run_pipeline(type="processed"): # Change to 'raw' or 'scrape'
    if type is "processed":
        polls = preprocessor.loadProcessed()
    if type is "scrape":
        polls = preprocessor.load(scraper)
    elif type is "raw":
        polls = preprocessor.load()    
       
    model1.fitData(polls)
    model1.ols_regression()
    model1.summary()


if __name__== "__main__":
    run_pipeline()