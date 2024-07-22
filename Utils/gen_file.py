import pandas as pd
from datetime import datetime, timedelta
from debug import debug
import globals

def dbg(msg):
    debug("gen_file-->"+str(msg))


def create_file(cherries_ticker_dtls):
    dbg("in create_file")
    with pd.ExcelWriter(str(globals.data_filepath) +str(globals.data_filename)) as writer:
        cherries_ticker_dtls.to_excel(writer, sheet_name='Early_Cherries', index=False)
        ##Fallen_Gems_Df.to_excel(writer, sheet_name='Fallen_Gems', index=False)
    dbg("in file created")
