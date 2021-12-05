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
df = getter.df[["Date", "ÖVP_SPÖ", "Institute_bin"]]
df[df["Institute_bin"] == 1].plot(x="Date", y="ÖVP_SPÖ",marker=6)
df[df["Institute_bin"] == 0].plot(x="Date", y="ÖVP_SPÖ", kind='scatter')

# %%
import matplotlib.pyplot as plt
import datetime as dt

fig = plt.figure()
ax = plt.axes()
ax.scatter("Date", "ÖVP", marker=6, data=getter.df[getter.df["Institute_bin"]==1], label="Research Affairs")
ax.scatter("Date", "ÖVP", marker=6, data=getter.df[getter.df["Institute_bin"]==0], label="Other Institutes")
ax.set_xlabel('Date')
ax.set_ylabel("Percentage Points")
ax.axvline(dt.datetime(2017, 5, 10), c='grey', ls="--", label='Amtsübernahme')
ax.legend()
ax.set_title('Difference in Voting Percentage Estimation')

# %%
