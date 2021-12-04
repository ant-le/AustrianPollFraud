# %% SetUp Logging 
import logging

logging.basicConfig(
    format="%(levelname)s\t %(asctime)s\t %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO, # change to logging.ERROR to only log errors
)
# %% Import classes
from scripts.data_scraper import Scraper
from scripts.data_preprocesser import Preprocesser
from scripts.data_plotter import Plotter
# %% Scripe Data from Source
scraper = Scraper()
dic, df = scraper.load()
polls = df.copy(deep=True)
# %% Preprocess Data 
preprocesser = Preprocesser(polls)
preprocesser.load()
# %% Plotting
plotter = Plotter(preprocesser.df)
plotter.scatterplot("ÖVP_SPÖ")