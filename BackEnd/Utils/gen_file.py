import pandas as pd
from BackEnd.Utils.debug import debug
from BackEnd.Utils import globals
from pathlib import Path


def dbg(msg):
    debug("gen_file-->" + str(msg))


def create_file(cherries_ticker_dtls):
    # Construct file path
    file_path = Path(__file__).parent.joinpath(globals.data_filepath, globals.data_filename)

    # Log the file path
    dbg(f"Creating file at: {file_path}")

    # Create directory if it does not exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write DataFrame to Excel file
    with pd.ExcelWriter(file_path) as writer:
        cherries_ticker_dtls.to_excel(writer, sheet_name='Early_Cherries', index=False)
        # Uncomment and adjust the line below if you have Fallen_Gems_Df to write
        # Fallen_Gems_Df.to_excel(writer, sheet_name='Fallen_Gems', index=False)

    dbg(f"File created successfully: {file_path}")
