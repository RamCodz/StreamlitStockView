import logging
from pathlib import Path
from Utils import globals  # Assuming globals contains dbg_filepath and dbg_filename

# Get the project root directory
project_root = Path(__file__).resolve().parent

# Construct the log file path
file_nm = project_root / globals.dbg_filepath / globals.dbg_filename


# Configure logging
logging.basicConfig(
    filename=str(file_nm),
    encoding='utf-8',
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG
)


def debug(msg):
    logging.debug(msg)


# Test the logger
if __name__ == "__main__":
    debug('This message should go to the log file')
