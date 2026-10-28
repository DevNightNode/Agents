# Jira Sprint Planner

A Jira agent that helps with sprint planning by pulling backlog items, estimating stories, and managing issues through the workflow.

## Features

This agent automates common sprint planning tasks in Jira:
- Search for backlog items using JQL queries
- Create new issues for sprint planning
- Transition issues through workflow states
- Add comments to track planning decisions

## Tools

The agent exposes the following tools to the LLM:

### `search_issues(query: str, max_results: int = 50)`
Search for Jira issues using a JQL query.

**Parameters:**
- `query` (str): JQL query string to search for issues
- `max_results` (int): Maximum number of results to return (default: 50)

**Returns:**
List of dictionaries containing issue information including key, summary, status, assignee, priority, and URL.

### `create_issue(project_key: str, summary: str, description: str, issuetype: str = "Story", priority: str = "Medium", assignee: Optional[str] = None, labels: Optional[List[str]] = None)`
Create a new Jira issue.

**Parameters:**
- `project_key` (str): Key of the project to create the issue in
- `summary` (str): Summary of the issue
- `description` (str): Detailed description of the issue
- `issuetype` (str): Type of issue (default: Story)
- `priority` (str): Priority level (default: Medium)
- `assignee` (Optional[str]): Username of assignee
- `labels` (Optional[List[str]]): List of labels to add to the issue

**Returns:**
Dictionary containing the created issue information.

### `transition_issue(issue_key: str, transition_name: str)`
Transition an issue to a new status.

**Parameters:**
- `issue_key` (str): Key of the issue to transition
- `transition_name` (str): Name of the transition to perform

**Returns:**
Dictionary containing the updated issue information.

### `add_comment(issue_key: str, comment: str)`
Add a comment to a Jira issue.

**Parameters:**
- `issue_key` (str): Key of the issue to comment on
- `comment` (str): Text of the comment to add

**Returns:**
Dictionary containing the comment information.

## Required Environment Variables

Create a `.env` file with the following variables:
