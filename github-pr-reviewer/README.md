# GitHub PR Reviewer Agent

An AI agent that reviews GitHub pull requests by analyzing diffs and providing feedback.

## Features

- Fetches pull request diffs from GitHub
- Analyzes changes for potential issues
- Posts review comments on risky changes
- Submits final review (approve or request changes)

## Tools

### 1. `get_pull_request_diff`
Fetches the complete diff of a pull request including file changes, additions, and deletions.

**Parameters:**
- `owner` (str): GitHub username or organization name
- `repo` (str): Repository name
- `pull_number` (int): Pull request number

### 2. `post_review_comment`
Posts a comment on a specific line of code in the pull request.

**Parameters:**
- `owner` (str): GitHub username or organization name
- `repo` (str): Repository name
- `pull_number` (int): Pull request number
- `commit_id` (str): The commit hash
- `path` (str): The file path
- `line` (int): The line number
- `comment` (str): The comment text

### 3. `submit_review`
Submits a final review on the pull request.

**Parameters:**
- `owner` (str): GitHub username or organization name
- `repo` (str): Repository name
- `pull_number` (int): Pull request number
- `comment` (str): The review comment
- `event` (str): The review event type ("APPROVE", "REQUEST_CHANGES", or "COMMENT")

## Required Environment Variables

- `GITHUB_TOKEN`: GitHub personal access token with repo permissions

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your GitHub token:
   ```
   GITHUB_TOKEN=your_github_token_here
   ```

3. Run the agent:
   ```
   python main.py owner repo pull_number
   ```

Example:
```
python main.py octocat Hello-World 123
```

## Requirements

- Python 3.7+
- GitHub personal access token with repo permissions
