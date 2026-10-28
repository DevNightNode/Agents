# Stripe Billing Agent

A billing support agent that interacts with the Stripe API using the Vercel AI SDK. This agent can find customers, list invoices, issue refunds, and cancel subscriptions.

## Features

- **Find Customer**: Search for customers by email or ID
- **List Invoices**: Retrieve a customer's invoices
- **Issue Refund**: Process refunds for specific invoices
- **Cancel Subscription**: Cancel subscriptions at the end of billing period

## Tools

### findCustomer
- **Description**: Find a Stripe customer by email or customer ID
- **Parameters**:
  - `query` (string): Customer email or ID to search for

### listInvoices
- **Description**: List invoices for a customer
- **Parameters**:
  - `customerId` (string): Stripe customer ID
  - `limit` (number, optional): Number of invoices to return (default: 10)

### issueRefund
- **Description**: Issue a refund for a specific invoice
- **Parameters**:
  - `invoiceId` (string): Stripe invoice ID to refund
  - `amount` (number, optional): Amount to refund in cents. If not specified, refunds full amount.

### cancelSubscription
- **Description**: Cancel a subscription
- **Parameters**:
  - `subscriptionId` (string): Stripe subscription ID to cancel
  - `cancelAtPeriodEnd` (boolean, optional): Cancel at the end of the current billing period (default: true)

## Environment Variables

Create a `.env` file with the following variables:

```
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
```

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables in `.env` file

3. Run the agent:
```bash
npm run dev
```

Or build and run:
```bash
npm run build
npm start
```

## Requirements

- Node.js 18+
- Stripe account with API keys
- OpenAI API key (configured via environment variables)
- TypeScript 5+
- npm or yarn
