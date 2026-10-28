# Claude Code Reviewer Agent

A code review agent built with the Claude Agent SDK that analyzes code changes and provides feedback.

## Overview

This agent automatically reviews code changes by:
- Identifying changed files in a git repository
- Running linters on modified files
- Providing code quality feedback
- Posting review comments to pull requests

## Tools

### `get_changed_files`
- **Description**: Get list of changed files in the current git repository
- **Parameters**: None
- **Usage**: Automatically detects which files have been modified in the current commit

### `post_review`
- **Description**: Post code review comments to a pull request or similar system
- **Parameters**:
  - `pr_url` (string): URL of the pull request
  - `comments` (array): Array of comment objects with file, line, and comment properties
- **Usage**: Posts review feedback to version control systems

### `run_linter`
- **Description**: Run a linter on a specific file
- **Parameters**:
  - `file_path` (string): Path to the file to lint
  - `linter` (string): Linter to use (default: flake8)
- **Usage**: Runs code quality checks on individual files

## Required Environment Variables

```bash
# No specific environment variables required for basic functionality
# The agent uses system tools like git and linters
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Agent

```bash
python main.py
```

## .claude Configuration

The agent creates the following configuration files:

### `.claude/settings.json`
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Grep", 
      "Bash",
      "mcp__code-reviewer__get_changed_files",
      "mcp__code-reviewer__post_review",
      "mcp__code-reviewer__run_linter"
    ],
    "deny": []
  }
}
```

### `.claude/agents/security-reviewer.md`
```markdown
---
name: Security Reviewer
description: Agent that focuses on security issues in code changes
tools:
  - Read
  - Grep
  - Bash
  - mcp__code-reviewer__get_changed_files
  - mcp__code-reviewer__run_linter
---
This agent focuses specifically on identifying security vulnerabilities in code changes.
```

## Features

- Git integration for detecting changed files
- Linter integration (flake8, eslint)
- File reading and grep capabilities
- Bash execution for system commands
- Subagent support for specialized review tasks
- Strict permission mode for security
- Configurable maximum conversation turns

## Requirements

- Python 3.8+
- Git installed
- Linters installed (flake8, eslint)
- Claude Agent SDK v0.1.0
