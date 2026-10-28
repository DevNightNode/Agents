import base64
import os
from email.message import EmailMessage
from typing import List, Dict, Any
from langchain_core.tools import tool
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.compose']

def encode_message(to: str, subject: str, body: str, in_reply_to: str = "") -> str:
    """Build an RFC 2822 message and base64url-encode it for the Gmail API."""
    msg = EmailMessage()
    msg["To"] = to
    msg["Subject"] = subject
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        msg["References"] = in_reply_to
    msg.set_content(body)
    return base64.urlsafe_b64encode(msg.as_bytes()).decode()


def get_gmail_service():
    """Get Gmail service with authentication"""
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

@tool
def list_unread() -> List[Dict[str, Any]]:
    """List all unread emails in the inbox with subject, sender, and snippet"""
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
    messages = results.get('messages', [])
    
    unread_emails = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = msg['payload']
        headers = payload['headers']
        
        email_data = {
            'id': message['id'],
            'subject': next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject'),
            'from': next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender'),
            'snippet': msg.get('snippet', 'No snippet available')
        }
        unread_emails.append(email_data)
    
    return unread_emails

@tool
def apply_label(message_id: str, label_name: str) -> str:
    """Apply a label to an email message"""
    service = get_gmail_service()
    
    # Create label if it doesn't exist
    try:
        label = service.users().labels().get(userId='me', id=label_name).execute()
    except:
        label = service.users().labels().create(
            userId='me',
            body={
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
        ).execute()
    
    # Apply label to message
    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'addLabelIds': [label['id']]}
    ).execute()
    
    return f"Applied label '{label_name}' to message {message_id}"

@tool
def draft_reply(message_id: str, draft_content: str) -> str:
    """Create a draft reply to an email message"""
    service = get_gmail_service()
    
    # Get original message to extract recipient
    original_msg = service.users().messages().get(userId='me', id=message_id).execute()
    payload = original_msg['payload']
    headers = payload['headers']
    
    # Extract recipient from original message
    to_header = next((h for h in headers if h['name'] == 'From'), None)
    if not to_header:
        return "Could not determine recipient for reply"
    
    to_email = to_header['value']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
    message_id_header = next((h['value'] for h in headers if h['name'].lower() == 'message-id'), '')
    if not subject.lower().startswith('re:'):
        subject = f"Re: {subject}"

    # Create the draft in the original thread
    service.users().drafts().create(
        userId='me',
        body={
            'message': {
                'raw': encode_message(to_email, subject, draft_content, message_id_header),
                'threadId': original_msg['threadId'],
            }
        }
    ).execute()

    return f"Created draft reply for message {message_id}"

@tool
def forward_email(message_id: str, recipient_email: str, forward_content: str = "") -> str:
    """Forward an email to another recipient"""
    service = get_gmail_service()
    
    # Get original message
    original_msg = service.users().messages().get(userId='me', id=message_id).execute()
    payload = original_msg['payload']
    headers = payload['headers']
    
    # Extract subject and sender
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
    from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
    
    # Create forwarded message
    forwarded_message = (
        f"Forwarded message:\n"
        f"From: {from_email}\n"
        f"Subject: {subject}\n\n"
        f"{forward_content}\n\n"
        f"--- Original message ---\n"
        f"{original_msg.get('snippet', 'No snippet available')}"
    )
    
    # Send forwarded message
    service.users().messages().send(
        userId='me',
        body={'raw': encode_message(recipient_email, f"Fwd: {subject}", forwarded_message)}
    ).execute()

    return f"Forwarded message {message_id} to {recipient_email}"
