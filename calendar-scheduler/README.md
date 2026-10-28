# Calendar Scheduler Agent

A LangChain.js agent that manages Google Calendar scheduling operations including finding free slots, creating events, and canceling meetings.

## Features

- **Find Free Slots**: Identify available time slots for meetings based on attendee availability
- **Create Events**: Schedule new calendar events with attendees, location, and reminders
- **Cancel Events**: Remove existing calendar events by ID

## Tools

### `find_free_slots`
Find available time slots for a meeting given time constraints and attendees.

**Parameters:**
- `start_time` (string): Start time in ISO format
- `end_time` (string): End time in ISO format  
- `duration_minutes` (number): Meeting duration in minutes
- `attendees` (array): List of attendee email addresses

### `create_event`
Create a new calendar event with specified details.

**Parameters:**
- `summary` (string): Event title
- `start_time` (string): Start time in ISO format
- `end_time` (string): End time in ISO format
- `attendees` (array): List of attendee email addresses
- `description` (string, optional): Event description
- `location` (string, optional): Event location

### `cancel_event`
Cancel an existing calendar event by event ID.

**Parameters:**
- `event_id` (string): The ID of the event to cancel

## Environment Variables

Create a `.env` file with the following variables:

```
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
GOOGLE_CALENDAR_USER=scheduler@yourcompany.com
OPENAI_API_KEY=your_openai_api_key_here
```

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables in `.env` file

3. Run the agent:
```bash
npm start "Schedule a 30-minute meeting with john@example.com for tomorrow"
```

## Requirements

- Node.js 18+
- Google Calendar API key
- OpenAI API key
- Valid Google Calendar access permissions
