import { execSync } from 'child_process';
import type { CallToolResult } from '@modelcontextprotocol/sdk/types.js';

export const git_diff = async ({ path, commit }: { path?: string; commit?: string }): Promise<CallToolResult> => {
  try {
    const repoPath = path || process.cwd();
    const commitArg = commit ? ` ${commit}` : '';
    const diff = execSync(`git diff${commitArg}`, { cwd: repoPath, encoding: 'utf-8' });
    return {
      content: [{
        type: 'text',
        text: diff.trim() || 'No differences'
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
