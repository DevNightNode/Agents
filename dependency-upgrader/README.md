# Dependency Upgrader Agent

A Node.js project maintenance agent that automatically checks for outdated dependencies, security vulnerabilities, and updates package versions while running tests to ensure everything still works.

## Features

- Checks for outdated dependencies using `npm outdated`
- Scans for security vulnerabilities using `npm audit`
- Updates dependency versions in `package.json`
- Runs tests to verify changes don't break functionality
- Uses AI to make intelligent decisions about which dependencies to update

## Tools

### npm_outdated
- **Description**: Runs `npm outdated` to check for outdated dependencies
- **Parameters**: 
  - `cwd` (optional): Working directory to run the command in

### npm_audit
- **Description**: Runs `npm audit` to check for security vulnerabilities
- **Parameters**: 
  - `cwd` (optional): Working directory to run the command in

### bump_dependency
- **Description**: Bumps a dependency version in package.json
- **Parameters**: 
  - `dependency`: Name of the dependency to bump
  - `version`: New version to bump to
  - `cwd` (optional): Working directory to run the command in

### run_tests
- **Description**: Runs `npm test` command
- **Parameters**: 
  - `cwd` (optional): Working directory to run the command in

## Required Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for the AI model

## How to Run

1. Install dependencies:
```bash
npm install
```

2. Build the project:
```bash
npm run build
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

4. Run the agent:
```bash
npm start
```

For development with auto-reload:
```bash
npm run dev
```

## Requirements

- Node.js 18+
- npm
- OpenAI API key
- A Node.js project with package.json in the working directory
