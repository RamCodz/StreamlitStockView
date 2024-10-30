import requests
import os
from base64 import b64encode
from io import StringIO
from datetime import datetime, timedelta

# Get the GitHub token from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Define the date threshold
threshold_date = datetime.now() - timedelta(days=30)

# Function to list files in the specified directory
def list_files_in_repo(url):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Returns a list of files and folders
    else:
        print(f"Error fetching files: {response.status_code} - {response.json()}")
        return []

# Function to delete a file in the repository
def delete_file(url, sha):
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
        print(f"Deleted {path}")
    else:
        print(f"Error deleting file {path}: {response.status_code} - {response.json()}")

# Main function to find and delete old CSV files
def delete_old_csv_files(url):
    files = list_files_in_repo(url)  # List files in the root directory (you can specify a subdirectory if needed)
    
    for file in files:
        if file["name"].endswith(".csv"):
            # Extract the date from the file name
            try:
                file_date_str = file["name"].split("_")[1].split(".")[0]  # Extract date from filename
                file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
                
                # Check if the file is older than one month
                if file_date < threshold_date:
                    delete_file(url, file["sha"])  # Delete the file if it's older than one month
            except (IndexError, ValueError) as e:
                print(f"Could not parse date from filename {file['name']}: {e}")

# Function to create or update a file in a GitHub repository
def create_or_update_file(path, content, message="Update file via Streamlit", branch="main"):
    print("Starting create_or_update_file...")
    print(f"GITHUB_TOKEN is : {str(GITHUB_TOKEN)}")
    
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
    delete_old_csv_files(url)
    print("Completed create_or_update_file...")

