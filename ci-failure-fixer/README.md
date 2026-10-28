# CI Failure Fixer Agent

A Python agent that automatically fixes CI failures by analyzing logs, cloning repos, running tests, applying fixes, and opening pull requests.

## Overview

The CI Failure Fixer agent is designed to automatically diagnose and fix CI build failures. It reads CI logs, clones the failing repository, runs the failing tests to reproduce the issue, applies necessary code fixes, and opens a pull request with the solution.

## Tools

The agent exposes the following tools to the LLM:

### 1. `get_ci_logs`
Fetches CI logs from a given URL.

**Parameters:**
- `ci_url` (str): The URL to the CI logs

**Returns:**
- The CI log content as a string

### 2. `clone_repo`
Clones a Git repository to a temporary directory.

**Parameters:**
- `repo_url` (str): The URL of the repository to clone
- `branch` (str, optional): The branch to checkout

**Returns:**
- Path to the cloned repository

### 3. `run_tests`
Runs a test command in a subprocess within the specified working directory.

**Parameters:**
- `test_command` (str): The command to run tests
- `working_dir` (str): The working directory to run the command in

**Returns:**
- The output of the test command

### 4. `apply_patch`
Applies a patch to files in the working directory.

**Parameters:**
- `patch_content` (str): The patch content to apply
- `working_dir` (str): The working directory where the patch should be applied

**Returns:**
- Status of the patch application

### 5. `open_pull_request`
Opens a pull request on GitHub.

**Parameters:**
- `title` (str): The title of the pull request
- `description` (str): The description of the pull request
- `base_branch` (str): The base branch to merge into
- `head_branch` (str, optional): The head branch to merge from

**Returns:**
- The URL of the created pull request or error message

## Required Environment Variables

- `GITHUB_TOKEN`: GitHub personal access token with repository permissions
- `OPENAI_API_KEY`: OpenAI API key for the LLM

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export GITHUB_TOKEN="your_github_token"
   export OPENAI_API_KEY="your_openai_api_key"
   ```

3. Run the agent:
   ```bash
   python main.py
   ```

## Example Usage

The agent can be invoked with a user input like:
```
Please fix this CI failure:
CI URL: https://ci.example.com/builds/12345
Test command: python -m pytest tests/
```

The agent will automatically:
1. Fetch the CI logs
2. Clone the repository
3. Run tests to reproduce the failure
4. Analyze the failure and create a fix
5. Apply the fix to the repository
6. Open a pull request with the fix

## Security Considerations

- The agent runs tests in a temporary directory with limited permissions
- All operations are contained within the agent's execution environment
- The agent does not have access to sensitive data beyond what's provided in the environment variables
- The agent only operates on repositories that are explicitly provided in the input
