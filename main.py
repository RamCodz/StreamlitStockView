import pandas as pd
from datetime import datetime, timedelta
##from predict_stk import filter_stocks  --
from debug import debug
import globals
from fetch_all_ticker_data import get_all_data
from early_cherries.early_cherries import find_cherries
from fallen_gems.fallen_gems import find_gems
from gen_file import create_file

def dbg(msg):
    debug("main-->"+str(msg))

globals.today = datetime.now().strftime(globals.dt_format)
globals.dbg_filename = str(globals.dbg_filename).replace("*", str(globals.today))
globals.data_filename = globals.data_filename.replace("*",str(globals.today))
dbg("*********************STARTED**************************")
dbg("in main module")
dbg("dbg filename "+globals.dbg_filename);

all_data = pd.DataFrame()
dbg("reading stocklist from csv")
StockList = pd.read_csv(str(globals.equity_list_path) + str(globals.equity_list_filename))

dbg("before fetching all tickers data ")
all_data = get_all_data(StockList)
dbg("after fetching all tickers data ")
all_data = all_data.rename_axis('Date').reset_index()## assigning first col name in df and make it as column
all_data['Date'] = pd.to_datetime(all_data['Date'])  

dbg("lets find Early cherries ")
cherries_ticker_dtls = find_cherries(all_data, StockList)
dbg("Early cherries completed ")

dbg("Lets find Fallen Gems")
##gems_ticker_dtls = fallen_gems(all_data, StockList)
dbg("Fallen Gems Completed")


##new dataframes can be added and the same needs to be handled in gen_file module
create_file(cherries_ticker_dtls)  

dbg("*********************COMPLETED**************************")