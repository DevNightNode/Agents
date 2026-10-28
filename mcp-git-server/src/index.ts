import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { git_status } from './tools/git_status.js';
import { git_diff } from './tools/git_diff.js';
import { git_log } from './tools/git_log.js';
import { git_commit } from './tools/git_commit.js';
import { git_checkout } from './tools/git_checkout.js';

const server = new McpServer({
  name: 'mcp-git-server',
  version: '1.0.0',
});

const repoPath = z
  .string()
  .optional()
  .describe('Path to the git repository (optional, defaults to current directory)');

server.registerTool('git_status', {
  title: 'Git Status',
  description: 'Get the status of the git repository, showing modified, added, and deleted files.',
  inputSchema: { path: repoPath },
}, git_status);

server.registerTool('git_diff', {
  title: 'Git Diff',
  description: 'Show changes between commits, working tree, and index.',
  inputSchema: {
    path: repoPath,
    commit: z.string().optional().describe('Commit hash to diff against (optional, defaults to HEAD)'),
  },
}, git_diff);

server.registerTool('git_log', {
  title: 'Git Log',
  description: 'Show commit logs with specified options.',
  inputSchema: {
    path: repoPath,
    limit: z.number().int().positive().optional().describe('Number of commits to show (optional, defaults to 10)'),
    format: z.string().optional().describe('Format of the log output (optional, defaults to short)'),
  },
}, git_log);

server.registerTool('git_commit', {
  title: 'Git Commit',
  description: 'Create a new commit with the specified message.',
  inputSchema: {
    path: repoPath,
    message: z.string().describe('Commit message'),
    author: z.string().optional().describe('Author name and email (optional)'),
  },
}, git_commit);

server.registerTool('git_checkout', {
  title: 'Git Checkout',
  description: 'Switch branches or restore working tree files.',
  inputSchema: {
    path: repoPath,
    branch: z.string().describe('Branch name to checkout'),
    create: z.boolean().optional().describe('Create new branch if it does not exist (optional, defaults to false)'),
  },
}, git_checkout);

await server.connect(new StdioServerTransport());
