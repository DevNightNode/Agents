import { execSync } from 'child_process';
import type { CallToolResult } from '@modelcontextprotocol/sdk/types.js';

export const git_log = async ({ path, limit = 10, format = 'short' }: { path?: string; limit?: number; format?: string }): Promise<CallToolResult> => {
  try {
    const repoPath = path || process.cwd();
    const formatArg = format === 'short' ? '--oneline' : `--format=${format}`;
    const log = execSync(`git log -n ${limit} ${formatArg}`, { cwd: repoPath, encoding: 'utf-8' });
    return {
      content: [{
        type: 'text',
        text: log.trim()
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
