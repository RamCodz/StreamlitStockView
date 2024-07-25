import requests
import os
from base64 import b64encode

# Get the GitHub token from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Function to create or update a file in a GitHub repository
def create_or_update_file(path, content, message="Update file via Streamlit", branch="main"):
    url = f"https://api.github.com/repos/RamCodz/StreamlitStockView/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Check if the file already exists to get the SHA
    response = requests.get(url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None

    data = {
        "message": message,
        "content": b64encode(content.encode("utf-8")).decode("utf-8"),
        "branch": branch
    }
    if sha:
        data["sha"] = sha

    response = requests.put(url, json=data, headers=headers)
