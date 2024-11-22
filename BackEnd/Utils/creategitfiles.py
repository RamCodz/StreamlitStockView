import requests
import os
from base64 import b64encode
from io import StringIO
from datetime import datetime, timedelta
import pandas as pd

# Get the GitHub token from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Define the date threshold for files to be deleted (older than 30 days)
THRESHOLD_DATE = datetime.now() - timedelta(days=30)

def list_files_in_repo(url):
    """List files in the specified GitHub repository directory."""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching files: {response.status_code} - {response.json()}")
        return []

def delete_file(file_path, sha):
    """Delete a file in the GitHub repository."""
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

def delete_old_files(base_url):
    """Find and delete old CSV files from the GitHub repository."""
    files = list_files_in_repo(base_url)
    
    for file in files:
        if isinstance(file, dict) and file.get("name").endswith(".csv"):
            try:
                file_date_str = file["name"].split("_")[1].split(".")[0]
                file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
                if file_date < THRESHOLD_DATE:
                    delete_file(file["path"], file["sha"])
            except (IndexError, ValueError) as e:
                print(f"Could not parse date from filename {file['name']}: {e}")

def create_or_delete_file(output_path, file_name, content, message="Update file via Streamlit", branch="main"):
    """Create or update a file in the GitHub repository."""
    
    path = os.path.join(output_path, file_name)
    if len(GITHUB_TOKEN) < 100:
        message = "Update file via Schedule"
    create_url = f"https://api.github.com/repos/RamCodz/StreamlitStockView/contents/{path}"
    delete_url = f"https://api.github.com/repos/RamCodz/StreamlitStockView/contents/{output_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(create_url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None
    
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
       
    delete_old_files(delete_url)
    
    response = requests.put(create_url, json=data, headers=headers)
    if response.status_code in (201, 200):
        print("File created or deleted successfully.")
    else:
        print(f"Error creating/updating file: {response.status_code} - {response.json()}")
       
