import os
import re
from datetime import datetime

def get_latest_file(folder_path):
    file_pattern = r'^StockView_(\d{4}-\d{2}-\d{2})\.csv$'  # Adjust the pattern as needed
  
    # Compile a regex pattern to match the file names
    pattern = re.compile(file_pattern)
    
    # Get list of files in the specified folder
    files = os.listdir(folder_path)
    
    # Filter files that match the pattern
    matched_files = [f for f in files if pattern.match(f)]
    
    # Extract dates from the file names and find the latest one
    latest_file = None
    latest_date = None
    
    for file in matched_files:
        # Extract date from the file name
        date_str = pattern.match(file).group(1)
        file_date = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Update the latest file if this file is newer
        if latest_date is None or file_date > latest_date:
            latest_date = file_date
            latest_file = file
    
    return latest_file
