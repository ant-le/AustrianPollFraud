# %% SetUp Logging 
import logging

logging.basicConfig(
    format="%(levelname)s\t %(asctime)s\t %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO, # change to logging.ERROR to only log errors
)
# %% Import classes
from scripts.data_plotter import Plotter
from scripts.data_getter import Getter
# %% Get Data
getter = Getter()
getter.getProcessedData()
# %% Plotting
plotter = Plotter(getter.df)
plotter.scatterplot("ÖVP_SPÖ")
# %%
