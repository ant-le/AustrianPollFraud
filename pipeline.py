# %% SetUp Logging
import logging

logging.basicConfig(
    format="%(levelname)s\t %(asctime)s\t %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO, # change to logging.ERROR to only log errors
)
# %%   # ------------------------- imports ------------------------- #
from scripts.data_getter import Getter
from scripts.data_handler import Handler
# %%   # ------------------------ init objs ------------------------ #
def run_pipeline(compare=False):
    # Dataset for comparison 
    if compare is True:
        getter_alt = Getter()
        getter_alt.getCheckData()
        handler = Handler(getter_alt.df)
        print("Check Dataset")
        handler.plotDifference("SPÖ")
        handler.naive_dif_in_dif("SPÖ", plot=True)
        
    getter = Getter()
    getter.getProcessedData()
    handler = Handler(getter.df)
    print("Initial Dataset")
    handler.plotDifference("Grüne")
    handler.naive_dif_in_dif("SPÖ", save=True)


if __name__== "__main__":
    run_pipeline()
# %%
import logging
import json
import requests
import pandas as pd
from requests.models import Response
from tqdm import tqdm

logging.info("Loadding data...")
try:
    response = requests.get("https://en.wikipedia.org/wiki/Opinion_polling_for_the_2017_Austrian_legislative_election")
except Exception as err:
    logging.error(f"Error while trying to read data: {err}")
if response.status_code == 200:
    logging.info(f"Status OK")
