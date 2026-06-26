# config.py
from dotenv import load_dotenv
import os
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME") or os.getenv("GITHUB_REPOSITORY_OWNER")

repo_env = os.getenv("GITHUB_REPO")
if not repo_env:
    repo_full = os.getenv("GITHUB_REPOSITORY")
    if repo_full and "/" in repo_full:
        repo_env = repo_full.split("/")[-1]
GITHUB_REPO = repo_env

LEETCODE_SESSION    = os.getenv("LEETCODE_SESSION")
LEETCODE_CSRF_TOKEN = os.getenv("LEETCODE_CSRF_TOKEN")