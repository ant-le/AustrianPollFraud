
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
from model.diff_in_diff import TwoWayFixedEffects
from model.bayesian_regression import BayesRegression
# ------------------------- init objs ------------------------- #
scraper = Scraper()
handler = Handler()
plotter = Plotter()
model_fr = TwoWayFixedEffects()
model = BayesRegression(att=True)
# ------------------------ run pipeline ------------------------ #
def run_pipeline():
    polls = handler.getSimulationData(att=True, noise=True)
    model.sample(polls, num_iter=15000, num_chains=3, num_thin=3, num_warmup=1500)
    plotter.trace(model)
    model.summary()
    plotter.posterior(model) 
    
if __name__== "__main__":
    run_pipeline()