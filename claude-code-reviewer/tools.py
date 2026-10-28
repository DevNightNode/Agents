import os
import subprocess
import json
import re

import requests
from typing import List, Dict, Any
from claude_agent_sdk import tool

@tool(
    "get_changed_files",
    "Get list of changed files in the current git repository",
    {}
)
async def get_changed_files(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get list of changed files in the current git repository"""
    try:
        # Get changed files using git diff
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        
        files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(files, indent=2)
                }
            ]
        }
    except subprocess.CalledProcessError as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error getting changed files: {str(e)}"
                }
            ]
        }

@tool(
    "post_review",
    "Post a review with inline comments to a GitHub pull request",
    {
        "type": "object",
        "properties": {
            "pr_url": {"type": "string", "description": "https://github.com/<owner>/<repo>/pull/<number>"},
            "summary": {"type": "string", "description": "Overall review summary"},
            "comments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string"},
                        "line": {"type": "integer"},
                        "comment": {"type": "string"},
                    },
                    "required": ["file", "line", "comment"],
                },
            },
        },
        "required": ["pr_url", "summary", "comments"],
    }
)
async def post_review(args: Dict[str, Any]) -> Dict[str, Any]:
    """Post a COMMENT review with inline comments to a GitHub pull request"""
    match = re.match(r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)", args.get("pr_url", ""))
    if not match:
        return {"content": [{"type": "text", "text": f"Not a GitHub pull request URL: {args.get('pr_url')}"}]}
    owner, repo, number = match.groups()

    response = requests.post(
        f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}/reviews",
        headers={
            "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
            "Accept": "application/vnd.github+json",
        },
        json={
            "event": "COMMENT",
            "body": args.get("summary", ""),
            "comments": [
                {"path": c["file"], "line": c["line"], "side": "RIGHT", "body": c["comment"]}
                for c in args.get("comments", [])
            ],
        },
        timeout=30,
    )
    if response.status_code >= 300:
        return {"content": [{"type": "text", "text": f"GitHub API error {response.status_code}: {response.text}"}]}

    review = response.json()
    return {
        "content": [
            {
                "type": "text",
                "text": f"Posted review {review['id']} with {len(args.get('comments', []))} comments: {review['html_url']}"
            }
        ]
    }

@tool(
    "run_linter",
    "Run a linter on a specific file",
    {
        "file_path": str,
        "linter": str
    }
)
async def run_linter(args: Dict[str, Any]) -> Dict[str, Any]:
    """Run a linter on a specific file"""
    file_path = args.get("file_path", "")
    linter = args.get("linter", "flake8")
    
    if not os.path.exists(file_path):
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"File not found: {file_path}"
                }
            ]
        }
    
    try:
        if linter == "flake8":
            result = subprocess.run(
                ["flake8", file_path],
                capture_output=True,
                text=True,
                check=False
            )
        elif linter == "eslint":
            result = subprocess.run(
                ["eslint", file_path],
                capture_output=True,
                text=True,
                check=False
            )
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Unsupported linter: {linter}"
                    }
                ]
            }
        
        if result.returncode == 0:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"No linting errors found in {file_path}"
                    }
                ]
            }
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Linting errors in {file_path}:\n{result.stdout}"
                    }
                ]
            }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error running linter: {str(e)}"
                }
            ]
        }
