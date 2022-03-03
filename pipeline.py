
# SetUp Logging
import logging
logging.basicConfig(
    format="%(levelname)s\t %(asctime)s\t %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO, # change to logging.ERROR to only log errors
)
# -------------------------- imports -------------------------- #
from scripts.scraper import Scraper
from scripts.preprocessor import Preprocessor
from scripts.plotter import Plotter
from model.diff_in_diff import TwoWayFixedEffects
from model.bayesian_regression import BayesRegression
# ------------------------- init objs ------------------------- #
scraper = Scraper()
preprocessor = Preprocessor()
plotter = Plotter()
model1 = TwoWayFixedEffects(test='t')
model2 = BayesRegression(impute=False)
model3 = BayesRegression()
# ------------------------ run pipeline ------------------------ #
def run_pipeline():
    polls = preprocessor.load(scraper)
    model1.fit(polls)
    model2.sample(polls)
    model3.sample(polls)
    

if __name__== "__main__":
    run_pipeline()