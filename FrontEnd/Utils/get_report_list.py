import os
import re

def get_file_names(folder_path):
    file_pattern = r'^StockView_(\d{4}-\d{2}-\d{2})\.csv$'
    # Compile a regex pattern to match the file names
    pattern = re.compile(file_pattern)
    
    # Get list of files in the specified folder
    files = os.listdir(folder_path)
    
    # Filter files that match the pattern
    matched_files = [f for f in files if pattern.match(f)]
    
    return matched_files
