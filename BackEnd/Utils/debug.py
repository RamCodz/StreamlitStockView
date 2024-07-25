import os 
from datetime import datetime
from BackEnd.Utils import globals
from BackEnd.Utils.creategitfiles import create_or_update_file

def debug(msg):
    #dbg_file = os.path.join(globals.dbg_filepath, str(globals.dbg_filename)) 
    #with open(dbg_file, 'a') as file:
        #file.write(str(datetime.now().strftime(globals.dt_time_format))+"--"+ str(msg) + '\n')
    create_or_update_file(str(globals.dbg_filepath) + str(globals.dbg_filename),msg)
