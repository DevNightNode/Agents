import os
from typing import List, Dict, Any, Optional
from jira import JIRA

# Initialize Jira client
jira_server = os.getenv("JIRA_SERVER")
jira_username = os.getenv("JIRA_USERNAME")
jira_api_token = os.getenv("JIRA_API_TOKEN")

if not all([jira_server, jira_username, jira_api_token]):
    raise ValueError("JIRA_SERVER, JIRA_USERNAME, and JIRA_API_TOKEN must be set in environment variables")

jira = JIRA(server=jira_server, basic_auth=(jira_username, jira_api_token))

async def search_issues(query: str, max_results: int = 50) -> List[Dict[str, Any]]:
    """
    Search for Jira issues using JQL query.
    
    Args:
        query: JQL query string to search for issues
        max_results: Maximum number of results to return (default: 50)
        
    Returns:
        List of dictionaries containing issue information
    """
    try:
        issues = jira.search_issues(query, maxResults=max_results)
        return [
            {
                "key": issue.key,
                "summary": issue.fields.summary,
                "status": issue.fields.status.name,
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
                "priority": issue.fields.priority.name if issue.fields.priority else "Unknown",
                "issuetype": issue.fields.issuetype.name,
                "description": issue.fields.description,
                "estimate": issue.fields.estimate,
                "url": f"{jira_server}/browse/{issue.key}"
            }
            for issue in issues
        ]
    except Exception as e:
        raise Exception(f"Failed to search issues: {str(e)}")

async def create_issue(
    project_key: str,
    summary: str,
    description: str,
    issuetype: str = "Story",
    priority: str = "Medium",
    assignee: Optional[str] = None,
    labels: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create a new Jira issue.
    
    Args:
        project_key: Key of the project to create the issue in
        summary: Summary of the issue
        description: Detailed description of the issue
        issuetype: Type of issue (default: Story)
        priority: Priority level (default: Medium)
        assignee: Username of assignee (optional)
        labels: List of labels to add to the issue (optional)
        
    Returns:
        Dictionary containing the created issue information
    """
    try:
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issuetype},
            'priority': {'name': priority}
        }
        
        if assignee:
            issue_dict['assignee'] = {'name': assignee}
            
        if labels:
            issue_dict['labels'] = labels
            
        issue = jira.create_issue(fields=issue_dict)
        
        return {
            "key": issue.key,
            "summary": issue.fields.summary,
            "status": issue.fields.status.name,
            "url": f"{jira_server}/browse/{issue.key}"
        }
    except Exception as e:
        raise Exception(f"Failed to create issue: {str(e)}")

async def transition_issue(issue_key: str, transition_name: str) -> Dict[str, Any]:
    """
    Transition an issue to a new status.
    
    Args:
        issue_key: Key of the issue to transition
        transition_name: Name of the transition to perform
        
    Returns:
        Dictionary containing the updated issue information
    """
    try:
        issue = jira.issue(issue_key)
        
        # Get available transitions
        transitions = jira.transitions(issue)
        transition_id = None
        
        for transition in transitions:
            if transition.name.lower() == transition_name.lower():
                transition_id = transition.id
                break
                
        if not transition_id:
            available_transitions = [t.name for t in transitions]
            raise Exception(f"Transition '{transition_name}' not found. Available transitions: {', '.join(available_transitions)}")
            
        # Perform the transition
        jira.transition_issue(issue, transition_id)
        
        # Refresh the issue to get updated status
        issue = jira.issue(issue_key)
        
        return {
            "key": issue.key,
            "summary": issue.fields.summary,
            "status": issue.fields.status.name,
            "url": f"{jira_server}/browse/{issue.key}"
        }
    except Exception as e:
        raise Exception(f"Failed to transition issue: {str(e)}")

async def add_comment(issue_key: str, comment: str) -> Dict[str, Any]:
    """
    Add a comment to a Jira issue.
    
    Args:
        issue_key: Key of the issue to comment on
        comment: Text of the comment to add
        
    Returns:
        Dictionary containing the comment information
    """
    try:
        issue = jira.issue(issue_key)
        comment_obj = jira.add_comment(issue, comment)
        
        return {
            "issue_key": issue_key,
            "comment_id": comment_obj.id,
            "comment_text": comment_obj.body,
            "author": comment_obj.author.displayName,
            "url": f"{jira_server}/browse/{issue_key}?focusedCommentId={comment_obj.id}#comment-{comment_obj.id}"
        }
    except Exception as e:
        raise Exception(f"Failed to add comment: {str(e)}")
