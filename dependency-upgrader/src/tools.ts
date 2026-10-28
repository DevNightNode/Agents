import { tool } from 'ai';
import { z } from 'zod';
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';

const execAsync = promisify(exec);

export const npm_outdated = tool({
  description: 'Runs npm outdated to check for outdated dependencies',
  parameters: z.object({
    cwd: z.string().optional().describe('Working directory to run the command in')
  }),
  execute: async ({ cwd = '.' }) => {
    try {
      const { stdout, stderr } = await execAsync('npm outdated', { cwd });
      return {
        success: true,
        output: stdout,
        error: stderr
      };
    } catch (error: any) {
      return {
        success: false,
        output: '',
        error: error.message || 'Unknown error occurred'
      };
    }
  }
});

export const npm_audit = tool({
  description: 'Runs npm audit to check for security vulnerabilities',
  parameters: z.object({
    cwd: z.string().optional().describe('Working directory to run the command in')
  }),
  execute: async ({ cwd = '.' }) => {
    try {
      const { stdout, stderr } = await execAsync('npm audit', { cwd });
      return {
        success: true,
        output: stdout,
        error: stderr
      };
    } catch (error: any) {
      return {
        success: false,
        output: '',
        error: error.message || 'Unknown error occurred'
      };
    }
  }
});

export const bump_dependency = tool({
  description: 'Bumps a dependency version in package.json',
  parameters: z.object({
    dependency: z.string().describe('Name of the dependency to bump'),
    version: z.string().describe('New version to bump to'),
    cwd: z.string().optional().describe('Working directory to run the command in')
  }),
  execute: async ({ dependency, version, cwd = '.' }) => {
    try {
      const packagePath = path.join(cwd, 'package.json');
      const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf-8'));
      
      if (packageJson.dependencies && packageJson.dependencies[dependency]) {
        packageJson.dependencies[dependency] = version;
      } else if (packageJson.devDependencies && packageJson.devDependencies[dependency]) {
        packageJson.devDependencies[dependency] = version;
      } else {
        return {
          success: false,
          error: `Dependency ${dependency} not found in package.json`
        };
      }
      
      fs.writeFileSync(packagePath, JSON.stringify(packageJson, null, 2));
      
      return {
        success: true,
        message: `Successfully bumped ${dependency} to version ${version}`
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Unknown error occurred'
      };
    }
  }
});

export const run_tests = tool({
  description: 'Runs npm test command',
  parameters: z.object({
    cwd: z.string().optional().describe('Working directory to run the command in')
  }),
  execute: async ({ cwd = '.' }) => {
    try {
      const { stdout, stderr } = await execAsync('npm test', { cwd });
      return {
        success: true,
        output: stdout,
        error: stderr
      };
    } catch (error: any) {
      return {
        success: false,
        output: '',
        error: error.message || 'Unknown error occurred'
      };
    }
  }
});
