import { execSync } from 'child_process';
import type { CallToolResult } from '@modelcontextprotocol/sdk/types.js';

export const git_commit = async ({ path, message, author }: { path?: string; message: string; author?: string }): Promise<CallToolResult> => {
  try {
    const repoPath = path || process.cwd();
    
    // Stage all changes
    execSync('git add .', { cwd: repoPath, encoding: 'utf-8' });
    
    // Commit with message
    const authorArg = author ? `--author="${author}"` : '';
    const commit = execSync(`git commit -m "${message}" ${authorArg}`, { cwd: repoPath, encoding: 'utf-8' });
    
    return {
      content: [{
        type: 'text',
        text: commit.trim()
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
