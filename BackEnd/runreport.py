import pandas as pd
from datetime import datetime
from Utils.debug import debug
from Utils import globals
from Utils.fetch_all_ticker_data import get_all_data
from EarlyCherries.early_cherries import find_cherries
from Utils.gen_file import create_file


def dbg(msg):
    debug("main-->" + str(msg))


def main():
    pass
