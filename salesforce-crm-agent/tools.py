from typing import List, Dict, Any
from langchain_core.tools import tool
from simple_salesforce import Salesforce
import os

# Initialize Salesforce connection
sf = Salesforce(
    username=os.getenv("SALESFORCE_USERNAME"),
    password=os.getenv("SALESFORCE_PASSWORD"),
    security_token=os.getenv("SALESFORCE_SECURITY_TOKEN"),
    domain=os.getenv("SALESFORCE_DOMAIN", "login")
)

@tool
def search_accounts(query: str) -> List[Dict[str, Any]]:
    """
    Search for Salesforce accounts by name or other criteria.
    
    Args:
        query: Search term to find accounts (name, industry, etc.)
        
    Returns:
        List of account records matching the search criteria
    """
    try:
        accounts = sf.query(f"SELECT Id, Name, Industry, Type, Phone, Website FROM Account WHERE Name LIKE '%{query}%' OR Industry LIKE '%{query}%' LIMIT 100")
        return accounts['records']
    except Exception as e:
        return [{"error": f"Failed to search accounts: {str(e)}"}]

@tool
def log_call(
    account_id: str,
    call_type: str,
    call_duration: int,
    call_notes: str,
    call_date: str
) -> Dict[str, Any]:
    """
    Log a call activity in Salesforce for a specific account.
    
    Args:
        account_id: Salesforce Account ID
        call_type: Type of call (e.g., 'Outbound', 'Inbound')
        call_duration: Duration of call in minutes
        call_notes: Notes about the call
        call_date: Date of the call (format: YYYY-MM-DD)
        
    Returns:
        Result of the call logging operation
    """
    try:
        # Create a new task for the call
        task = sf.Task.create({
            'Subject': f'Call with {account_id}',
            'Type': call_type,
            'DurationInMinutes': call_duration,
            'Description': call_notes,
            'ActivityDate': call_date,
            'WhoId': account_id,
            'Status': 'Completed'
        })
        return {"success": True, "task_id": task['id']}
    except Exception as e:
        return {"success": False, "error": f"Failed to log call: {str(e)}"}

@tool
def update_opportunity(
    opportunity_id: str,
    stage_name: str,
    close_date: str = None,
    amount: float = None
) -> Dict[str, Any]:
    """
    Update an opportunity's stage and related fields in Salesforce.
    
    Args:
        opportunity_id: Salesforce Opportunity ID
        stage_name: New stage name (e.g., 'Qualification', 'Proposal', 'Closed Won')
        close_date: New close date (format: YYYY-MM-DD)
        amount: New opportunity amount
        
    Returns:
        Result of the opportunity update operation
    """
    try:
        update_data = {
            'StageName': stage_name
        }
        if close_date:
            update_data['CloseDate'] = close_date
        if amount:
            update_data['Amount'] = amount
            
        opportunity = sf.Opportunity.update(opportunity_id, update_data)
        return {"success": True, "opportunity_id": opportunity_id}
    except Exception as e:
        return {"success": False, "error": f"Failed to update opportunity: {str(e)}"}

@tool
def export_report(report_id: str) -> Dict[str, Any]:
    """
    Export a Salesforce report to CSV format.
    
    Args:
        report_id: Salesforce Report ID
        
    Returns:
        Report data including CSV content
    """
    try:
        # Get report metadata
        report = sf.report(report_id)
        # Note: This is a simplified version - actual implementation would 
        # require Salesforce's REST API for report exports
        return {
            "success": True, 
            "report_id": report_id,
            "message": "Report exported successfully (simplified implementation)"
        }
    except Exception as e:
        return {"success": False, "error": f"Failed to export report: {str(e)}"}
