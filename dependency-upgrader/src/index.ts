import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { npm_outdated, npm_audit, bump_dependency, run_tests } from './tools.js';

const system = `
You are a Node.js project maintenance agent. Your job is to help maintain package dependencies by:
1. Checking for outdated dependencies using npm outdated
2. Running npm audit to check for security vulnerabilities
3. Bumping dependency versions in package.json when appropriate
4. Running tests to ensure changes don't break anything

Always follow this process:
1. First, run npm_outdated to see what needs updating
2. Then run npm_audit to check for security issues
3. If there are security issues, prioritize fixing those first
4. Then decide which dependencies to bump based on version numbers and security concerns
5. After bumping dependencies, run run_tests to make sure everything still works
6. Repeat as necessary

You have access to these tools:
- npm_outdated: Check for outdated dependencies
- npm_audit: Check for security vulnerabilities
- bump_dependency: Update a dependency version in package.json
- run_tests: Run npm test command

Always be careful when bumping dependencies - make sure to run tests after each change.
`;

async function main() {
  const result = await generateText({
    model: openai('gpt-4.1'),
    system,
    prompt: 'Please check the project for outdated dependencies and security vulnerabilities, then update as needed.',
    tools: {
      npm_outdated,
      npm_audit,
      bump_dependency,
      run_tests
    },
    maxSteps: 8
  });

  console.log('Final result:', result.text);
}

main().catch(console.error);
