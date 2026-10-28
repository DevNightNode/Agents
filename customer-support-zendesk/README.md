# Customer Support Zendesk Agent

A LangChain-powered customer support agent that integrates with Zendesk to search help center articles, look up ticket history, and draft/send replies to customers.

## Features

- Search Zendesk help center for relevant articles
- Retrieve detailed ticket information
- Reply to tickets with public or private messages
- Escalate tickets by assigning to agents/groups or changing priority

## Tools

1. **search_help_center(query: str, limit: int = 10)**
   - Searches the Zendesk help center for articles matching the query
   - Returns list of articles with title, URL, excerpt, and creation date

2. **get_ticket(ticket_id: int)**
   - Retrieves a specific ticket by ID
   - Returns comprehensive ticket information including subject, description, status, priority, requester details, and comments

3. **reply_to_ticket(ticket_id: int, message: str, is_public: bool = True)**
   - Replies to a Zendesk ticket with a message
   - Can be set as public (visible to customer) or private

4. **escalate_ticket(ticket_id: int, assignee_id: Optional[int] = None, group_id: Optional[int] = None, priority: Optional[str] = None)**
   - Escalates a ticket by assigning it to an agent/group or changing its priority
   - Accepts one or more of assignee_id, group_id, or priority parameters

## Required Environment Variables

Create a `.env` file with the following variables:

```
ZENDESK_SUBDOMAIN=your_subdomain
ZENDESK_EMAIL=your_email@example.com
ZENDESK_API_TOKEN=your_api_token
OPENAI_API_KEY=your_openai_api_key
```

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env` file

3. Run the agent:
   ```
   python main.py
   ```

## Usage

The agent will prompt you for queries. You can ask it to:
- Search for help center articles
- Look up ticket details
- Reply to tickets
- Escalate tickets

Example interactions:
- "Find articles about password reset"
- "Get ticket #12345 details"
- "Reply to ticket #12345 with 'We've reset your password'"
- "Escalate ticket #12345 to the billing group"

## Security Notes

- All API credentials are loaded from environment variables
- The agent uses official Zendesk API endpoints
- No sensitive data is stored or logged
