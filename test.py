import streamlit as st
import requests
import os
from base64 import b64encode

# Get the GitHub token from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Function to create or update a file in a GitHub repository
def create_or_update_file(repo, path, content, message="Update file via Streamlit", branch="main"):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
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
    if response.status_code in [200, 201]:
        st.success("File created/updated successfully")
    else:
        st.error(f"Failed to create/update file: {response.json()}")

# Streamlit app UI
st.title("GitHub File Uploader")

repo = st.text_input("Repository (e.g., username/repo)")
path = st.text_input("File Path (e.g., folder/filename.txt)")
content = st.text_area("File Content")

if st.button("Upload"):
    if GITHUB_TOKEN and repo and path and content:
        create_or_update_file(repo, path, content)
    else:
        st.error("Please fill in all fields and ensure the token is set.")
