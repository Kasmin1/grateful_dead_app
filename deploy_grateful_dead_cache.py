import os
import subprocess
import webbrowser
import time

GITHUB_USERNAME = "Kasmin1"
REPO_NAME = "grateful_dead_app"
BRANCH = "main"

if not os.path.exists(".git"):
    subprocess.run(["git", "init"])

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "deploy"])

subprocess.run(["git", "remote", "remove", "origin"], stderr=subprocess.DEVNULL)

subprocess.run([
    "git", "remote", "add", "origin",
    f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
])

subprocess.run(["git", "branch", "-M", BRANCH])
subprocess.run(["git", "push", "-u", "origin", BRANCH])

url = f"https://share.streamlit.io/{GITHUB_USERNAME}/{REPO_NAME}/{BRANCH}/app_deadhead_api.py"

print("Open this in browser:", url)
webbrowser.open(url)