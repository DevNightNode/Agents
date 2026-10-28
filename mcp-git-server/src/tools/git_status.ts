import { execSync } from 'child_process';
import type { CallToolResult } from '@modelcontextprotocol/sdk/types.js';

export const git_status = async ({ path }: { path?: string }): Promise<CallToolResult> => {
  try {
    const repoPath = path || process.cwd();
    const status = execSync('git status --porcelain', { cwd: repoPath, encoding: 'utf-8' });
    return {
      content: [{
        type: 'text',
        text: status.trim() || 'No changes'
      }]
    };
  } catch (error: any) {
    return {
      content: [{
        type: 'text',
        text: `Error: ${error.message}`
      }]
    };
  }
};
