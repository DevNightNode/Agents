import os
import tempfile
import subprocess
import shutil
import re
import time
from typing import Optional, List, Dict, Any
from pathlib import Path
from agents import function_tool
import requests
import git
from github import Github

# Environment variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Global variables for tracking
repo_path = None
repo = None

@function_tool
def get_ci_logs(ci_url: str) -> str:
    """
    Fetches CI logs from a given URL.
    
    Args:
        ci_url (str): The URL to the CI logs
        
    Returns:
        str: The CI log content
    """
    try:
        response = requests.get(ci_url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Failed to fetch CI logs: {str(e)}"

@function_tool
def clone_repo(repo_url: str, branch: Optional[str] = None) -> str:
    """
    Clones a Git repository to a temporary directory.
    
    Args:
        repo_url (str): The URL of the repository to clone
        branch (str, optional): The branch to checkout
        
    Returns:
        str: Path to the cloned repository
    """
    global repo_path, repo
    
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    repo_path = Path(temp_dir) / "repo"
    
    try:
        # Clone the repository
        repo = git.Repo.clone_from(repo_url, repo_path)
        
        # Checkout specific branch if provided
        if branch:
            repo.git.checkout(branch)
            
        return str(repo_path)
    except Exception as e:
        return f"Failed to clone repository: {str(e)}"

@function_tool
def run_tests(test_command: str, working_dir: str) -> str:
    """
    Runs a test command in a subprocess within the specified working directory.
    
    Args:
        test_command (str): The command to run tests
        working_dir (str): The working directory to run the command in
        
    Returns:
        str: The output of the test command
    """
    try:
        # Run the test command
        result = subprocess.run(
            test_command,
            shell=True,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        output = f"Return code: {result.returncode}\n"
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
            
        return output
    except subprocess.TimeoutExpired:
        return "Test command timed out after 5 minutes"
    except Exception as e:
        return f"Failed to run tests: {str(e)}"

@function_tool
def apply_patch(patch_content: str, working_dir: str) -> str:
    """
    Applies a patch to files in the working directory.
    
    Args:
        patch_content (str): The patch content to apply
        working_dir (str): The working directory where the patch should be applied
        
    Returns:
        str: Status of the patch application
    """
    try:
        # Create a temporary patch file
        patch_file = os.path.join(working_dir, "temp_patch.patch")
        with open(patch_file, "w") as f:
            f.write(patch_content)
        
        # Apply the patch using git
        result = subprocess.run(
            ["git", "apply", patch_file],
            cwd=working_dir,
            capture_output=True,
            text=True
        )
        
        # Clean up the temporary patch file
        os.remove(patch_file)
        
        if result.returncode == 0:
            return "Patch applied successfully"
        else:
            return f"Failed to apply patch: {result.stderr}"
    except Exception as e:
        return f"Failed to apply patch: {str(e)}"

@function_tool
def open_pull_request(
    repo_full_name: str,
    title: str,
    description: str,
    base_branch: str = "main",
    head_branch: Optional[str] = None
) -> str:
    """
    Commits the patched working tree of the cloned repository to a new branch,
    pushes it, and opens a pull request on GitHub.
    
    Args:
        repo_full_name (str): The GitHub repository as "owner/name"
        title (str): The title of the pull request (also the commit message)
        description (str): The description of the pull request
        base_branch (str): The base branch to merge into
        head_branch (str, optional): The branch to push the fix to
        
    Returns:
        str: The URL of the created pull request or error message
    """
    try:
        if not GITHUB_TOKEN:
            return "GITHUB_TOKEN environment variable not set"
        if repo is None:
            return "No repository cloned"
        
        if not head_branch:
            head_branch = f"ci-fix-{int(time.time())}"
        
        # Commit the applied patch on a new branch and push it
        repo.git.checkout("-b", head_branch)
        repo.git.add(A=True)
        repo.index.commit(title)
        push_url = f"https://x-access-token:{GITHUB_TOKEN}@github.com/{repo_full_name}.git"
        repo.git.push(push_url, f"{head_branch}:{head_branch}")
        
        gh_repo = Github(GITHUB_TOKEN).get_repo(repo_full_name)
        pr = gh_repo.create_pull(
            title=title,
            body=description,
            head=head_branch,
            base=base_branch
        )
        
        return f"Pull request created: {pr.html_url}"
    except Exception as e:
        return f"Failed to open pull request: {str(e)}"
