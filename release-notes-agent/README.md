# Ruby Release Notes Agent

An AI-powered release notes generator that automatically creates GitHub releases with properly categorized commit messages.

## Overview

This agent uses the Claude 4-5 model to analyze git commits since the last tag and automatically generates release notes with proper categorization. It then creates a GitHub release with those notes.

## Features

- Automatically detects the latest git tag
- Groups commits by type (features, fixes, refactors, etc.)
- Creates properly formatted release notes
- Publishes release to GitHub
- Uses Claude 4-5 for intelligent categorization

## Tools

### `list_commits_since_tag`
- **Description**: Lists all git commits since a given tag
- **Parameters**:
  - `tag` (string): The git tag to compare against
- **Returns**: List of commit information with SHA, author, and message

### `create_release`
- **Description**: Creates a GitHub release using the GitHub API
- **Parameters**:
  - `tag` (string): The tag name for the release
  - `title` (string): The release title
  - `body` (string): The release body/description
  - `is_prerelease` (boolean, optional): Whether this is a pre-release
- **Returns**: The created release information

## Required Environment Variables

- `GITHUB_TOKEN`: GitHub personal access token with repository permissions

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment:
   ```bash
   cp .env.example .env
   # Edit .env to add your GITHUB_TOKEN
   ```

3. Run the agent:
   ```bash
   python main.py v1.5.0   # new tag; the previous tag is detected with git describe
   ```

## How It Works

1. The agent determines the latest git tag using `git describe --tags --abbrev=0`
2. It fetches all commits since that tag using `git log`
3. Commits are categorized based on message prefixes:
   - Features: `feat:`, `feature:`, `add:`, `new:`
   - Fixes: `fix:`, `bug:`, `resolve:`, `fixes:`
   - Refactors: `refactor:`, `refactorings:`, `restructure:`, `reorganize:`
   - Documentation: `docs:`, `doc:`, `documentation:`, `readme:`
   - Tests: `test:`, `tests:`, `testing:`, `unit:`
   - Chores: Everything else
4. The agent formats the release notes in a structured way
5. It creates a GitHub release with the formatted notes

## Example Output

```
## Features
- Add user authentication feature
- Implement payment processing

## Fixes
- Fix login validation bug
- Resolve database connection issue

## Refactors
- Restructure API endpoints
- Improve code organization

## Documentation
- Update README with installation instructions
- Add API documentation

## Tests
- Add unit tests for user module
- Implement integration tests
```
