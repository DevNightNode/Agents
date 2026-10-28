import os
from typing import Optional, List
from github import Github
from agents import function_tool

# Initialize GitHub client
github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GITHUB_TOKEN environment variable is required")
g = Github(github_token)

@function_tool
def get_pull_request_diff(
    owner: str,
    repo: str,
    pull_number: int
) -> str:
    """
    Fetches the diff of a GitHub pull request.
    
    Args:
        owner: The GitHub username or organization name
        repo: The repository name
        pull_number: The pull request number
        
    Returns:
        The full diff content as a string
    """
    try:
        repo_obj = g.get_repo(f"{owner}/{repo}")
        pr = repo_obj.get_pull(pull_number)
        diff = pr.get_files()
        diff_content = []
        for file in diff:
            diff_content.append(f"File: {file.filename}")
            diff_content.append(f"Status: {file.status}")
            diff_content.append(f"Additions: {file.additions}")
            diff_content.append(f"Deletions: {file.deletions}")
            diff_content.append(f"Diff URL: {file.patch_url}")
            diff_content.append("---")
            diff_content.append(file.patch)
            diff_content.append("\n")
        return "\n".join(diff_content)
    except Exception as e:
        return f"Error fetching PR diff: {str(e)}"

@function_tool
def post_review_comment(
    owner: str,
    repo: str,
    pull_number: int,
    commit_id: str,
    path: str,
    line: int,
    comment: str
) -> str:
    """
    Posts a review comment on a specific line of a pull request.
    
    Args:
        owner: The GitHub username or organization name
        repo: The repository name
        pull_number: The pull request number
        commit_id: The commit hash
        path: The file path
        line: The line number
        comment: The comment text
        
    Returns:
        Success message or error
    """
    try:
        repo_obj = g.get_repo(f"{owner}/{repo}")
        pr = repo_obj.get_pull(pull_number)
        pr.create_review_comment(
            comment=comment,
            commit_id=commit_id,
            path=path,
            line=line
        )
        return f"Successfully posted comment on PR #{pull_number}"
    except Exception as e:
        return f"Error posting review comment: {str(e)}"

@function_tool
def submit_review(
    owner: str,
    repo: str,
    pull_number: int,
    comment: str,
    event: str = "COMMENT"
) -> str:
    """
    Submits a review on a pull request.
    
    Args:
        owner: The GitHub username or organization name
        repo: The repository name
        pull_number: The pull request number
        comment: The review comment
        event: The review event type ("APPROVE", "REQUEST_CHANGES", or "COMMENT")
        
    Returns:
        Success message or error
    """
    try:
        repo_obj = g.get_repo(f"{owner}/{repo}")
        pr = repo_obj.get_pull(pull_number)
        pr.create_review(
            commit_id=pr.head.sha,
            body=comment,
            event=event
        )
        return f"Successfully submitted review on PR #{pull_number} with event {event}"
    except Exception as e:
        return f"Error submitting review: {str(e)}"
