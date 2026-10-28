import { ChatOpenAI } from '@langchain/openai';
import { createReactAgent } from '@langchain/langgraph/prebuilt';
import { get_inventory, update_price, create_discount_code } from './tools.js';
import { Config } from './config.js';

const llm = new ChatOpenAI({
  model: 'gpt-4-turbo',
  temperature: 0,
  openAIApiKey: Config.OPENAI_API_KEY,
});

const tools = [
  get_inventory,
  update_price,
  create_discount_code,
];

const prompt = `You are a Shopify store management agent. You can:
1. Check inventory levels for products
2. Update product prices
3. Create discount codes

Always use the appropriate tool for each request. Be precise with product IDs and variant IDs.
`;

const agent = createReactAgent({
  llm,
  tools,
  prompt,
});

async function main() {
  const userInput = process.argv.slice(2).join(' ');
  if (!userInput) {
    console.error('Usage: npm run dev -- "<store request>"');
    process.exit(1);
  }
  console.log(`User input: ${userInput}`);
  
  try {
    const result = await agent.invoke(
      { messages: [{ role: 'user', content: userInput }] },
      { recursionLimit: 20 }
    );
    console.log('Agent response:', JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('Error running agent:', error);
  }
}

main();
