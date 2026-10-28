import subprocess
import os
import re

import requests
from typing import List, Dict, Any


def list_commits_since_tag(tag: str) -> List[Dict[str, str]]:
    """
    List commits since a given git tag.
    
    Args:
        tag (str): The git tag to compare against
        
    Returns:
        List[Dict[str, str]]: List of commit information with 'sha', 'message', and 'author'
    """
    try:
        # Get commits since the tag
        result = subprocess.run(
            ["git", "log", "--format=%H|%an|%s", f"{tag}..HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                sha, author, message = line.split('|', 2)
                commits.append({
                    'sha': sha,
                    'author': author,
                    'message': message
                })
        
        return commits
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to get commits since tag {tag}: {e}")

def create_release(tag: str, title: str, body: str, is_prerelease: bool = False) -> Dict[str, Any]:
    """
    Create a GitHub release using the GitHub API.
    
    Args:
        tag (str): The tag name for the release
        title (str): The release title
        body (str): The release body/description
        is_prerelease (bool): Whether this is a pre-release
        
    Returns:
        Dict[str, Any]: The created release information
    """
    # Get GitHub token from environment
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise Exception("GITHUB_TOKEN environment variable is required")
    
    # Get repository info from git
    try:
        repo_url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
        
        # Extract owner and repo name from URL
        match = re.search(r'github\.com[:/](.*?)/([^/]*?)(?:\.git)?$', repo_url)
        if not match:
            raise Exception("Could not determine repository owner and name from git remote")
            
        owner, repo = match.groups()
    except subprocess.CalledProcessError:
        raise Exception("Could not determine repository from git remote")
    
    # Create release using GitHub API

    
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "tag_name": tag,
        "name": title,
        "body": body,
        "draft": False,
        "prerelease": is_prerelease
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=30)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create release: {response.status_code} - {response.text}")
    
    return response.json()
