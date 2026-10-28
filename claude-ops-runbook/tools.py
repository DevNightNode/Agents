import os
import subprocess
import time
import requests
from typing import Dict, Any
from claude_agent_sdk import tool

# Datadog API configuration
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")
DATADOG_APP_KEY = os.getenv("DATADOG_APP_KEY")
DATADOG_SITE = os.getenv("DATADOG_SITE", "datadoghq.com")
DATADOG_API_URL = f"https://api.{DATADOG_SITE}"

# PagerDuty API configuration
PAGERDUTY_API_KEY = os.getenv("PAGERDUTY_API_KEY")
PAGERDUTY_API_URL = "https://api.pagerduty.com"
PAGERDUTY_FROM_EMAIL = os.getenv("PAGERDUTY_FROM_EMAIL", "")

@tool(
    "query_metrics",
    "Query a Datadog metric (e.g. avg:trace.http.request.errors{service:web}) over the last N minutes",
    {
        "query": str,
        "minutes_back": int
    }
)
async def query_metrics(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Query Datadog timeseries metrics.
    
    Args:
        query (str): Datadog metrics query, e.g. avg:system.cpu.user{service:web}
        minutes_back (int): How many minutes of history to fetch
        
    Returns:
        dict: Response from Datadog API with metrics data
    """
    if not DATADOG_API_KEY or not DATADOG_APP_KEY:
        return {"content": [{"type": "text", "text": "Error: DATADOG_API_KEY and DATADOG_APP_KEY must be set"}]}
    
    headers = {
        "DD-API-KEY": DATADOG_API_KEY,
        "DD-APPLICATION-KEY": DATADOG_APP_KEY
    }
    
    url = f"{DATADOG_API_URL}/api/v1/query"
    
    now = int(time.time())
    params = {
        "from": now - int(args["minutes_back"]) * 60,
        "to": now,
        "query": args["query"]
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return {"content": [{"type": "text", "text": f"Datadog metrics query results: {data}"}]}
    except requests.RequestException as e:
        return {"content": [{"type": "text", "text": f"Error querying Datadog metrics: {str(e)}"}]}

@tool(
    "get_incident",
    "Get details of a PagerDuty incident by ID",
    {
        "incident_id": str
    }
)
async def get_incident(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get details of a PagerDuty incident by ID.
    
    Args:
        incident_id (str): The ID of the incident to retrieve
        
    Returns:
        dict: Incident details from PagerDuty
    """
    if not PAGERDUTY_API_KEY:
        return {"content": [{"type": "text", "text": "Error: PAGERDUTY_API_KEY not set"}]}
    
    headers = {
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Authorization": f"Token token={PAGERDUTY_API_KEY}"
    }
    
    url = f"{PAGERDUTY_API_URL}/incidents/{args['incident_id']}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {"content": [{"type": "text", "text": f"Incident details: {data}"}]}
    except requests.RequestException as e:
        return {"content": [{"type": "text", "text": f"Error retrieving incident: {str(e)}"}]}

@tool(
    "acknowledge_incident",
    "Acknowledge a PagerDuty incident by ID",
    {
        "incident_id": str
    }
)
async def acknowledge_incident(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Acknowledge a PagerDuty incident by ID.
    
    Args:
        incident_id (str): The ID of the incident to acknowledge
        
    Returns:
        dict: Acknowledgment result
    """
    if not PAGERDUTY_API_KEY:
        return {"content": [{"type": "text", "text": "Error: PAGERDUTY_API_KEY not set"}]}
    
    headers = {
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Authorization": f"Token token={PAGERDUTY_API_KEY}",
        "Content-Type": "application/json",
        "From": PAGERDUTY_FROM_EMAIL
    }
    
    url = f"{PAGERDUTY_API_URL}/incidents/{args['incident_id']}"
    
    payload = {
        "incident": {
            "type": "incident",
            "status": "acknowledged"
        }
    }
    
    try:
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return {"content": [{"type": "text", "text": f"Incident acknowledged successfully: {data}"}]}
    except requests.RequestException as e:
        return {"content": [{"type": "text", "text": f"Error acknowledging incident: {str(e)}"}]}

@tool(
    "restart_service",
    "Restart a service by name",
    {
        "service_name": str
    }
)
async def restart_service(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Restart a service by name using systemctl.
    
    Args:
        service_name (str): The name of the service to restart
        
    Returns:
        dict: Result of the restart command
    """
    try:
        result = subprocess.run(
            ["sudo", "systemctl", "restart", args["service_name"]],
            capture_output=True,
            text=True,
            check=True
        )
        return {"content": [{"type": "text", "text": f"Service {args['service_name']} restarted successfully. Output: {result.stdout}"}]}
    except subprocess.CalledProcessError as e:
        return {"content": [{"type": "text", "text": f"Error restarting service {args['service_name']}: {e.stderr}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Unexpected error restarting service: {str(e)}"}]}
