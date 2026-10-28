import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { BrowserAutomationAgent } from './agent.js';

const server = new McpServer({ name: 'browser-automation-agent', version: '1.0.0' });

const agent = new BrowserAutomationAgent();

server.registerTool('navigate', {
  title: 'Navigate to URL',
  description: 'Navigate the browser to a specific URL',
  inputSchema: {
    url: z.string().describe('The URL to navigate to')
  }
}, async ({ url }) => {
  const result = await agent.navigate(url);
  return {
    content: [{
      type: 'text',
      text: result
    }]
  };
});

server.registerTool('click', {
  title: 'Click element',
  description: 'Click on an element identified by a CSS selector',
  inputSchema: {
    selector: z.string().describe('CSS selector of the element to click')
  }
}, async ({ selector }) => {
  const result = await agent.click(selector);
  return {
    content: [{
      type: 'text',
      text: result
    }]
  };
});

server.registerTool('fill', {
  title: 'Fill input field',
  description: 'Fill an input field with text using a CSS selector',
  inputSchema: {
    selector: z.string().describe('CSS selector of the input field'),
    text: z.string().describe('Text to fill into the input field')
  }
}, async ({ selector, text }) => {
  const result = await agent.fill(selector, text);
  return {
    content: [{
      type: 'text',
      text: result
    }]
  };
});

server.registerTool('screenshot', {
  title: 'Take screenshot',
  description: 'Take a screenshot of the current page and return it as base64',
  inputSchema: {
    path: z.string().describe('Path to save the screenshot (optional)')
  }
}, async ({ path }) => {
  const result = await agent.screenshot(path);
  return {
    content: [{
      type: 'text',
      text: result
    }]
  };
});

server.registerTool('get_text', {
  title: 'Extract text from element',
  description: 'Extract text content from an element identified by CSS selector',
  inputSchema: {
    selector: z.string().describe('CSS selector of the element to extract text from')
  }
}, async ({ selector }) => {
  const result = await agent.getText(selector);
  return {
    content: [{
      type: 'text',
      text: result
    }]
  };
});

await server.connect(new StdioServerTransport());
