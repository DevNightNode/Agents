import { createSdkMcpServer, query } from '@anthropic-ai/claude-agent-sdk';
import { listExports, readSource, writeDoc } from './tools.js';

// Create the MCP server with our tools
const server = createSdkMcpServer({
  name: 'claude-ts-docs-writer',
  version: '1.0.0',
  tools: [listExports, readSource, writeDoc]
});

// System prompt for the agent
const systemPrompt = `
You are a TypeScript documentation assistant. Your job is to read codebases and generate comprehensive API documentation.

You have access to three tools:
1. list_exports - Lists all exported functions, classes, and variables from a TypeScript file
2. read_source - Reads and returns the source code from a file
3. write_doc - Writes documentation to a file

When asked to generate documentation:
1. First, use list_exports to understand what's exported from a file
2. Then, use read_source to read the actual implementation
3. Finally, use write_doc to create documentation files

Always follow these guidelines:
- Generate comprehensive documentation for all exported members
- Include function signatures, parameters, return types, and descriptions
- Use clear, consistent formatting
- Make sure documentation is accurate to the actual code
- When in doubt, prefer the actual code over assumptions
`;

// Main agent execution
async function main() {
  const prompt = process.argv.slice(2).join(' ');
  if (!prompt) {
    console.error('Usage: npm start -- "<what to document, e.g. document the exports in src/api>"');
    process.exit(1);
  }
  
  console.log('Starting Claude TS Docs Writer agent...');
  console.log('Prompt:', prompt);
  
  try {
    for await (const message of query({
      prompt,
      options: {
        systemPrompt,
        mcpServers: {
          'claude-ts-docs-writer': server
        },
        allowedTools: [
          'mcp__claude-ts-docs-writer__list_exports',
          'mcp__claude-ts-docs-writer__read_source',
          'mcp__claude-ts-docs-writer__write_doc',
          'Read',
          'Grep'
        ],
        maxTurns: 20
      }
    })) {
      if (message.type === 'assistant') {
        for (const block of message.message.content) {
          if (block.type === 'text') {
            console.log(block.text);
          } else if (block.type === 'tool_use') {
            console.log(`Tool use: ${block.name}`);
          }
        }
      } else if (message.type === 'result') {
        console.log(`Finished after ${message.num_turns} turns`);
      }
    }
  } catch (error) {
    console.error('Error running agent:', error);
  }
}

main();
