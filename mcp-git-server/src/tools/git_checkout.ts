import { execSync } from 'child_process';
import type { CallToolResult } from '@modelcontextprotocol/sdk/types.js';

export const git_checkout = async ({ path, branch, create = false }: { path?: string; branch: string; create?: boolean }): Promise<CallToolResult> => {
  try {
    const repoPath = path || process.cwd();
    const createArg = create ? '-b' : '';
    const checkout = execSync(`git checkout ${createArg} ${branch}`, { cwd: repoPath, encoding: 'utf-8' });
    return {
      content: [{
        type: 'text',
        text: checkout.trim()
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
