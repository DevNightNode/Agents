import asyncio
import os
from typing import Optional
from langchain_core.tools import tool
from google.oauth2 import service_account
from googleapiclient.discovery import build
from okta.client import Client as OktaClient
import requests

# Google Workspace setup
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
GOOGLE_ADMIN_EMAIL = os.getenv("GOOGLE_ADMIN_EMAIL")

# Okta setup
OKTA_ORG_URL = os.getenv("OKTA_ORG_URL")
OKTA_API_TOKEN = os.getenv("OKTA_API_TOKEN")

# Email setup
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")

def get_google_service():
    """Initialize Google Admin SDK service."""
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/admin.directory.user',
                'https://www.googleapis.com/auth/admin.directory.group']
    )
    credentials = credentials.with_subject(GOOGLE_ADMIN_EMAIL)
    return build('admin', 'directory_v1', credentials=credentials)

def get_okta_client():
    """Initialize Okta client."""
    return OktaClient({"orgUrl": OKTA_ORG_URL, "token": OKTA_API_TOKEN})

@tool
def create_workspace_user(
    first_name: str,
    last_name: str,
    email: str,
    department: str,
    job_title: str,
    manager_email: Optional[str] = None
) -> str:
    """
    Create a new user in Google Workspace.
    
    Args:
        first_name: First name of the new user
        last_name: Last name of the new user
        email: Email address for the new user
        department: Department the user belongs to
        job_title: Job title of the user
        manager_email: Email of the user's manager (optional)
        
    Returns:
        User ID of the created user
    """
    try:
        service = get_google_service()
        user_body = {
            'name': {
                'givenName': first_name,
                'familyName': last_name,
                'fullName': f"{first_name} {last_name}"
            },
            'primaryEmail': email,
            'password': 'TempPassword123!',
            'changePasswordAtNextLogin': True,
            'orgUnitPath': f"/{department}",
            'emails': [{'address': email, 'type': 'work'}],
            'phones': [{'value': '', 'type': 'work'}],
            'organizations': [{'name': department, 'title': job_title, 'primary': True}],
            'suspended': False
        }
        
        if manager_email:
            user_body['manager'] = manager_email
            
        user = service.users().insert(body=user_body).execute()
        return f"Successfully created Google Workspace user with ID: {user['id']}"
    except Exception as e:
        return f"Error creating Google Workspace user: {str(e)}"

@tool
def create_okta_user(
    first_name: str,
    last_name: str,
    email: str,
    department: str,
    job_title: str,
    manager_email: Optional[str] = None
) -> str:
    """
    Create a new user in Okta.
    
    Args:
        first_name: First name of the new user
        last_name: Last name of the new user
        email: Email address for the new user
        department: Department the user belongs to
        job_title: Job title of the user
        manager_email: Email of the user's manager (optional)
        
    Returns:
        Okta user ID
    """
    try:
        client = get_okta_client()
        user_body = {
            'profile': {
                'firstName': first_name,
                'lastName': last_name,
                'email': email,
                'login': email,
                'department': department,
                'title': job_title
            },
            'credentials': {
                'password': {
                    'value': 'TempPassword123!'
                }
            }
        }
        
        if manager_email:
            user_body['profile']['manager'] = manager_email
            
        # The Okta SDK is async and returns (result, response, error)
        user, _, err = asyncio.run(client.create_user(user_body))
        if err:
            return f"Error creating Okta user: {err}"
        return f"Successfully created Okta user with ID: {user.id}"
    except Exception as e:
        return f"Error creating Okta user: {str(e)}"

@tool
def add_to_group(
    user_email: str,
    group_name: str
) -> str:
    """
    Add a user to a Google Workspace group.
    
    Args:
        user_email: Email of the user to add
        group_name: Name of the group to add the user to
        
    Returns:
        Success message
    """
    try:
        service = get_google_service()
        
        # First, get the group key
        group = service.groups().get(groupKey=group_name).execute()
        group_key = group['id']
        
        # Then add the user to the group
        member = {
            'email': user_email,
            'role': 'MEMBER'
        }
        
        service.members().insert(groupKey=group_key, body=member).execute()
        return f"Successfully added {user_email} to group {group_name}"
    except Exception as e:
        return f"Error adding user to group: {str(e)}"

@tool
def send_welcome_email(
    recipient_email: str,
    recipient_name: str,
    welcome_message: str,
    company_name: str
) -> str:
    """
    Send a welcome email to a new hire.
    
    Args:
        recipient_email: Email address of the recipient
        recipient_name: Name of the recipient
        welcome_message: Custom welcome message
        company_name: Name of the company
        
    Returns:
        Success message
    """
    try:
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={"Authorization": f"Bearer {EMAIL_API_KEY}"},
            json={
                "personalizations": [{"to": [{"email": recipient_email, "name": recipient_name}]}],
                "from": {"email": EMAIL_SENDER, "name": company_name},
                "subject": f"Welcome to {company_name}!",
                "content": [{
                    "type": "text/plain",
                    "value": f"Dear {recipient_name},\n\n{welcome_message}\n\nBest regards,\n{company_name} Team",
                }],
            },
            timeout=15,
        )
        response.raise_for_status()
        return f"Successfully sent welcome email to {recipient_email}"
    except Exception as e:
        return f"Error sending welcome email: {str(e)}"
