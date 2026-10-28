import { tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';
import fs from 'fs/promises';
import path from 'path';
import { exec } from 'child_process';

// Tool to list exports from a TypeScript file
export const listExports = tool(
  'list_exports',
  'Lists all exported functions, classes, and variables from a TypeScript file',
  {
    file_path: z.string().describe('Path to the TypeScript file'),
  },
  async ({ file_path }) => {
    try {
      const content = await fs.readFile(file_path, 'utf-8');
      
      // Simple regex to find exports
      const exportRegex = /export\s+(?:async\s+)?(?:function|class|const|let|var)\s+([a-zA-Z0-9_$]+)/g;
      const matches = [];
      let match;
      
      while ((match = exportRegex.exec(content)) !== null) {
        matches.push(match[1]);
      }
      
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(matches, null, 2)
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: 'text',
          text: `Error reading file: ${error instanceof Error ? error.message : String(error)}`
        }]
      };
    }
  }
);

// Tool to read source code from a file
export const readSource = tool(
  'read_source',
  'Reads and returns the source code from a file',
  {
    file_path: z.string().describe('Path to the file to read'),
  },
  async ({ file_path }) => {
    try {
      const content = await fs.readFile(file_path, 'utf-8');
      return {
        content: [{
          type: 'text',
          text: content
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: 'text',
          text: `Error reading file: ${error instanceof Error ? error.message : String(error)}`
        }]
      };
    }
  }
);

// Tool to write documentation to a file
export const writeDoc = tool(
  'write_doc',
  'Writes documentation to a file',
  {
    file_path: z.string().describe('Path to the documentation file'),
    content: z.string().describe('Documentation content to write'),
  },
  async ({ file_path, content }) => {
    try {
      // Ensure directory exists
      const dir = path.dirname(file_path);
      await fs.mkdir(dir, { recursive: true });
      
      await fs.writeFile(file_path, content, 'utf-8');
      return {
        content: [{
          type: 'text',
          text: `Successfully wrote documentation to ${file_path}`
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: 'text',
          text: `Error writing file: ${error instanceof Error ? error.message : String(error)}`
        }]
      };
    }
  }
);
