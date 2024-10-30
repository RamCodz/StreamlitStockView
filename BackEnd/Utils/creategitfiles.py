import streamlit as st
import requests
import os
from base64 import b64encode
from io import StringIO

# Get the GitHub token from environment variables
GITHUB_TOKEN = "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" #os.getenv("GITHUB_TOKEN")

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
    print("Completed create_or_update_file...")
