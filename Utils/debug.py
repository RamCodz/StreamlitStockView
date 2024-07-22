import os 
from datetime import datetime
import Utils.globals

def debug(msg):
    dbg_file = os.path.join(globals.dbg_filepath, str(globals.dbg_filename)) 
    with open(dbg_file, 'a') as file:
        file.write(str(datetime.now().strftime(globals.dt_time_format))+"--"+ str(msg) + '\n')
