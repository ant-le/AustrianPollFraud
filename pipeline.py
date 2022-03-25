
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
from model.bayesian_regression import BayesRegression
# ------------------------- init objs ------------------------- #
scraper = Scraper()
handler = Handler()
ovp = BayesRegression()
spo = BayesRegression('SPÖ')
# ------------------------ run pipeline ------------------------ #
def run_pipeline():
    handler.loadData()
    handler.scatter(var='SPÖ', binning=True, save=True)
    handler.scatter(binning=True, save=True)
    for model in [ovp,spo]:
        model.sample(handler.data)
        model.summary(latex=True)
        model.short_term(save=True)
        model.long_term(save=True)
        model.evaluate(save=True)
        model.trace(save=True)
        model.trends(handler.data, save=True)
        
    
if __name__== "__main__":
    run_pipeline()