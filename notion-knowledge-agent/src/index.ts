import { Agent, run } from '@openai/agents';
import { search_pages, read_page, append_block } from './notion-tools.js';

const agent = new Agent({
  name: 'Notion Knowledge Agent',
  instructions: `You are a helpful assistant that can search Notion pages, read their content, and append new content to pages. 
  When users ask questions, use the tools to find and retrieve information from Notion.
  If a user asks to add information to a page, use the append_block tool.
  Always be precise and helpful in your responses.`,
  model: 'gpt-4.1',
  tools: [search_pages, read_page, append_block]
});

async function main() {
  console.log('Notion Knowledge Agent started. Type your question or "exit" to quit.');
  
  while (true) {
    const input = process.argv[2];
    if (!input || input.toLowerCase() === 'exit') break;
    
    try {
      const result = await run(agent, input, { maxTurns: 10 });
      console.log('Final Output:', result.finalOutput);
    } catch (error) {
      console.error('Error:', error);
    }
    
    break;
  }
}

main();
