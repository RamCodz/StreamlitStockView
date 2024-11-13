import requests
import os
from base64 import b64encode
from io import StringIO
from datetime import datetime, timedelta

# Get the GitHub token from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Define the date threshold for files to be deleted (older than 30 days)
threshold_date = datetime.now() - timedelta(days=30)

# Function to list files in the specified directory
def list_files_in_repo(url):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Print the response for debugging
        return response.json()  # Returns a list of files and folders
    else:
        print(f"Error fetching files: {response.status_code} - {response.json()}")
        return []

# Function to delete a file in the repository
def delete_file(file_path, sha):
    url = f"https://api.github.com/repos/RamCodz/StreamlitStockView/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": "Delete old CSV file",
        "sha": sha
    }
    response = requests.delete(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"Deleted {file_path}")
    else:
        print(f"Error deleting file {file_path}: {response.status_code} - {response.json()}")

# Main function to find and delete old CSV files
def delete_old_csv_files(base_url):
    files = list_files_in_repo(base_url)  # List files in the root directory
    
    for file in files:
        # Check if the response item is a dictionary
        if isinstance(file, dict) and file.get("name").endswith(".csv"):
            # Extract the date from the file name
            try:
                file_date_str = file["name"].split("_")[1].split(".")[0]  # Extract date from filename
                file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
                
                # Check if the file is older than one month
                if file_date < threshold_date:
                    delete_file(file["path"], file["sha"])  # Delete the file if it's older than one month
            except (IndexError, ValueError) as e:
                print(f"Could not parse date from filename {file['name']}: {e}")

# Function to create or update a file in a GitHub repository
def create_or_update_file(path, content, message="Update file via Streamlit", branch="main"):
    print("Starting create_or_update_file...")
    print(path)
    if len(GITHUB_TOKEN) < 100:
         message="Update file via Schedule"
    url = f"https://api.github.com/repos/RamCodz/StreamlitStockView/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Check if the file already exists to get the SHA
    response = requests.get(url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None
    
    # Convert DataFrame to CSV
    csv_buffer = StringIO()
    content.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue()
    
    data = {
        "message": message,
        "content": b64encode(csv_content.encode("utf-8")).decode("utf-8"),
        "branch": branch
    }
    if sha:
        data["sha"] = sha

    response = requests.put(url, json=data, headers=headers)
    if response.status_code in (201, 200):
        print("File created or updated successfully.")
    else:
        print(f"Error creating/updating file: {response.status_code} - {response.json()}")
    
    # Call the function to delete old CSV files after updating the file
    #delete_old_csv_files(url)

    print("Completed create_or_update_file...")

# Example usage:
# If you have a DataFrame named 'df', you can call the function like this:
# create_or_update_file("path/to/your/file.csv", df)
