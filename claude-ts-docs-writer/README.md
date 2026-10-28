# Claude TS Docs Writer

A TypeScript Claude Agent SDK agent that reads codebases and generates comprehensive API documentation.

## Overview

This agent helps developers automatically generate and maintain API documentation for TypeScript projects. It can analyze codebases, extract exports, read source code, and write documentation files.

## Tools

### 1. `list_exports`
Lists all exported functions, classes, and variables from a TypeScript file.

**Parameters:**
- `file_path` (string): Path to the TypeScript file

**Example:**
```json
{
  "file_path": "./src/api.ts"
}
```

### 2. `read_source`
Reads and returns the source code from a file.

**Parameters:**
- `file_path` (string): Path to the file to read

**Example:**
```json
{
  "file_path": "./src/utils.ts"
}
```

### 3. `write_doc`
Writes documentation to a file.

**Parameters:**
- `file_path` (string): Path to the documentation file
- `content` (string): Documentation content to write

**Example:**
```json
{
  "file_path": "./docs/api.md",
  "content": "# API Documentation\n\n## Function: exampleFunction"
}
```

## Required Environment Variables

No environment variables required for basic operation.

## How to Run

### Development
```bash
npm run dev
```

### Build and Run
```bash
npm run build
npm start
```

### Usage
The agent can be invoked with a prompt:
```bash
npm start "Generate documentation for the entire project"
```

## Project Structure

```
.
├── package.json
├── tsconfig.json
├── src/
│   ├── tools.ts          # Tool implementations
│   └── index.ts          # Main agent entrypoint
└── README.md
```

## Features

- **Code Analysis**: Automatically discovers exports from TypeScript files
- **Source Reading**: Reads actual source code for accurate documentation
- **Documentation Generation**: Creates well-formatted documentation files
- **MCP Integration**: Uses Claude Agent SDK's MCP protocol for tool execution
- **Type Safety**: Full TypeScript support with Zod validation

## Requirements

- Node.js 16+
- npm or yarn

## License

MIT
