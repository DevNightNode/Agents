# Salesforce CRM Agent

A LangChain-powered AI agent that assists sales teams with Salesforce CRM operations. The agent can search accounts, log calls, update opportunities, and export reports.

## Features

- **Account Search**: Find Salesforce accounts by name or industry
- **Call Logging**: Log call activities with duration, type, and notes
- **Opportunity Management**: Update opportunity stages, close dates, and amounts
- **Report Export**: Export Salesforce reports (simplified implementation)

## Tools

### search_accounts
Search for Salesforce accounts matching a query term.

**Parameters:**
- `query` (str): Search term to find accounts (name, industry, etc.)

### log_call
Log a call activity in Salesforce for a specific account.

**Parameters:**
- `account_id` (str): Salesforce Account ID
- `call_type` (str): Type of call (e.g., 'Outbound', 'Inbound')
- `call_duration` (int): Duration of call in minutes
- `call_notes` (str): Notes about the call
- `call_date` (str): Date of the call (format: YYYY-MM-DD)

### update_opportunity
Update an opportunity's stage and related fields in Salesforce.

**Parameters:**
- `opportunity_id` (str): Salesforce Opportunity ID
- `stage_name` (str): New stage name (e.g., 'Qualification', 'Proposal', 'Closed Won')
- `close_date` (str, optional): New close date (format: YYYY-MM-DD)
- `amount` (float, optional): New opportunity amount

### export_report
Export a Salesforce report to CSV format.

**Parameters:**
- `report_id` (str): Salesforce Report ID

## Required Environment Variables

Create a `.env` file with the following variables:

```
OPENAI_API_KEY=your_openai_api_key_here
SALESFORCE_USERNAME=your_salesforce_username
SALESFORCE_PASSWORD=your_salesforce_password
SALESFORCE_SECURITY_TOKEN=your_salesforce_security_token
SALESFORCE_DOMAIN=login  # or test for sandbox
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env` file

3. Run the agent:
```bash
python main.py
```

## Usage

The agent will prompt you for requests. Examples include:
- "Find all accounts in the technology industry"
- "Log a 30-minute outbound call with account ABC123 about product demo"
- "Update opportunity XYZ123 to stage 'Proposal' with close date 2023-12-31"
- "Export the monthly sales report"

## Security Notes

- This agent requires direct access to Salesforce credentials
- Ensure environment variables are properly secured
- Consider implementing additional authentication layers for production use
