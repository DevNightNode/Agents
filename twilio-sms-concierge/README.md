# Twilio SMS Concierge

A restaurant reservation concierge agent that operates over SMS using Twilio. The agent can check table availability, book tables, and send confirmation SMS messages.

## Features

- **SMS-based interaction**: Customers can book tables by sending SMS messages
- **AI-powered assistant**: Uses GPT-4.1 to understand customer requests and manage reservations
- **Full reservation workflow**: Check availability, book tables, and send confirmations
- **Twilio integration**: Seamlessly integrates with Twilio for SMS communication

## Tools

### 1. `checkAvailability`
Checks if a table is available for a given date and time.

**Parameters:**
- `date` (string): Date in YYYY-MM-DD format
- `time` (string): Time in HH:MM format
- `partySize` (number): Number of people in the party

### 2. `bookTable`
Books a table for a given date and time.

**Parameters:**
- `date` (string): Date in YYYY-MM-DD format
- `time` (string): Time in HH:MM format
- `partySize` (number): Number of people in the party
- `customerName` (string): Name of the customer
- `customerPhone` (string): Phone number of the customer

### 3. `sendSms`
Sends an SMS message to a phone number.

**Parameters:**
- `to` (string): Phone number to send SMS to
- `message` (string): Message content

## Required Environment Variables

Create a `.env` file with the following variables:

```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
OPENAI_API_KEY=your_openai_api_key
PORT=3000
```

## Setup and Running

1. Install dependencies:
```bash
npm install
```

2. Set up your environment variables in `.env`

3. Start the server:
```bash
npm run dev
```

The server will start on port 3000 and listen for incoming SMS messages at `/webhook`.

## How It Works

1. Customer sends an SMS to your Twilio number with a reservation request
2. The server receives the message at the webhook endpoint
3. The AI agent processes the message using the available tools
4. The agent checks availability, books the table, and sends a confirmation SMS
5. The customer receives a confirmation message with their booking details

## Example Usage

Customer sends: "I want to book a table for 4 people on Friday at 7 PM"

Agent responds with: "Checking availability for 4 people on Friday at 7 PM..."
Then: "Table available! Booking confirmed for 4 people on Friday at 7 PM. Booking ID: BK-123456789"
Finally: "Confirmation sent to your phone"

## Notes

- This is a simplified implementation for demonstration
- In production, you would connect the tools to real databases and APIs
- The Twilio integration is configured to work with your Twilio account
- The AI agent uses GPT-4.1 for natural language understanding and processing
- Error handling is included for production use
