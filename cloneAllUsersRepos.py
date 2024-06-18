# Description: python command line script to clone all public repositories for a given user based on passed github username
import sys
import requests
import subprocess
import os

def fetch_github_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            clone_url = repo['clone_url']
            clone_repository(clone_url)
    else:
        print(f"Failed to fetch repositories: {response.status_code} - {response.text}")

def clone_repository(clone_url):
    # Extract repository name from clone_url
    repo_name = clone_url.split('/')[-1].split('.git')[0]
    if os.path.exists(repo_name):
        print(f"Repository '{repo_name}' already exists locally. Skipping clone.")
    else:
        try:
            subprocess.run(['git', 'clone', clone_url])
            print(f"Successfully cloned repository: {clone_url}")
        except Exception as e:
            print(f"Failed to clone repository: {clone_url} - {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <github_username>")
        sys.exit(1)
    
    github_username = sys.argv[1]
    fetch_github_repos(github_username)
