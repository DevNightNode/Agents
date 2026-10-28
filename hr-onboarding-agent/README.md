# HR Onboarding Agent

An AI-powered HR onboarding agent that automates the creation of user accounts in Google Workspace and Okta, assigns groups, and sends welcome emails to new hires.

## Features

This agent automates the entire new hire onboarding process by:
1. Creating user accounts in Google Workspace
2. Creating user accounts in Okta
3. Assigning users to appropriate groups
4. Sending personalized welcome emails

## Tools

### 1. `create_workspace_user`
Creates a new user in Google Workspace with the specified details.

**Parameters:**
- `first_name` (str): First name of the new user
- `last_name` (str): Last name of the new user
- `email` (str): Email address for the new user
- `department` (str): Department the user belongs to
- `job_title` (str): Job title of the user
- `manager_email` (str, optional): Email of the user's manager

### 2. `create_okta_user`
Creates a new user in Okta with the specified details.

**Parameters:**
- `first_name` (str): First name of the new user
- `last_name` (str): Last name of the new user
- `email` (str): Email address for the new user
- `department` (str): Department the user belongs to
- `job_title` (str): Job title of the user
- `manager_email` (str, optional): Email of the user's manager

### 3. `add_to_group`
Adds a user to a Google Workspace group.

**Parameters:**
- `user_email` (str): Email of the user to add
- `group_name` (str): Name of the group to add the user to

### 4. `send_welcome_email`
Sends a welcome email to a new hire.

**Parameters:**
- `recipient_email` (str): Email address of the recipient
- `recipient_name` (str): Name of the recipient
- `welcome_message` (str): Custom welcome message
- `company_name` (str): Name of the company

## Required Environment Variables

Create a `.env` file with the following variables:

```env
# Google Workspace
GOOGLE_CREDENTIALS_PATH=/path/to/service-account-key.json
GOOGLE_ADMIN_EMAIL=admin@yourcompany.com

# Okta
OKTA_ORG_URL=https://yourcompany.okta.com
OKTA_API_TOKEN=your-okta-api-token

# Email
EMAIL_SENDER=hr@yourcompany.com
EMAIL_API_KEY=your-sendgrid-api-key
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in a `.env` file

3. Run the agent:
```bash
python main.py
```

## Usage

The agent can be invoked with natural language instructions. For example:

```
Create a new user for John Smith in the Engineering department with job title Software Engineer. Add him to the Engineering group and send a welcome email.
```

The agent will automatically determine which tools to use and in what order to complete the onboarding process.
