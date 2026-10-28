import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { findCustomer, listInvoices, issueRefund, cancelSubscription } from './tools.js';

const system = `
You are a Stripe billing support agent. You can help customers with:
- Finding customer information
- Listing customer invoices
- Issuing refunds
- Cancelling subscriptions

Always be clear and precise in your responses. When using tools, make sure to provide all required arguments.
`;

async function main() {
  const prompt = process.argv.slice(2).join(' ');
  if (!prompt) {
    console.error('Usage: npm start -- "<billing request>"');
    process.exit(1);
  }

  const { text } = await generateText({
    model: openai('gpt-4.1'),
    system,
    prompt,
    tools: {
      findCustomer,
      listInvoices,
      issueRefund,
      cancelSubscription,
    },
    maxSteps: 8,
  });

  console.log(text);
}

main().catch(console.error);
