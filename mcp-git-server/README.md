# mcp-git-server

An MCP server that wraps Git operations for use with AI agents.

## Overview

This server exposes Git functionality as tools that can be called by LLM agents. It provides a standardized interface for common Git operations including status, diff, log, commit, and checkout.

## Tools

### `git_status`
Get the status of the git repository, showing modified, added, and deleted files.

**Parameters:**
- `path` (string, optional): Path to the git repository (defaults to current directory)

### `git_diff`
Show changes between commits, working tree, and index.

**Parameters:**
- `path` (string, optional): Path to the git repository (defaults to current directory)
- `commit` (string, optional): Commit hash to diff against (defaults to HEAD)

### `git_log`
Show commit logs with specified options.

**Parameters:**
- `path` (string, optional): Path to the git repository (defaults to current directory)
- `limit` (number, optional): Number of commits to show (defaults to 10)
- `format` (string, optional): Format of the log output (defaults to short)

### `git_commit`
Create a new commit with the specified message.

**Parameters:**
- `path` (string, optional): Path to the git repository (defaults to current directory)
- `message` (string): Commit message
- `author` (string, optional): Author name and email

### `git_checkout`
Switch branches or restore working tree files.

**Parameters:**
- `path` (string, optional): Path to the git repository (defaults to current directory)
- `branch` (string): Branch name to checkout
- `create` (boolean, optional): Create new branch if it does not exist (defaults to false)

## Requirements

- Node.js 16+
- Git installed and available in PATH
- A Git repository to operate on

## Setup

1. Install dependencies:
```bash
npm install
```

2. Build the project:
```bash
npm run build
```

## Running

To run the server:
```bash
npm start
```

The server will communicate via stdio and can be used with any MCP-compatible client.

## Environment Variables

This server does not require any environment variables to run, but it will operate on the current working directory unless a specific path is provided to each tool.

## Usage Example

```bash
# Get repository status
mcp call git_status

# Show diff against HEAD
mcp call git_diff

# Show last 5 commits
mcp call git_log --limit 5

# Commit with message
mcp call git_commit --message "Update documentation"

# Checkout branch
mcp call git_checkout --branch feature-branch
```
