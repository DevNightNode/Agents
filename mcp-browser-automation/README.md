# MCP Browser Automation Agent

An MCP server that drives a headless Playwright browser for automation tasks.

## Overview

This agent provides a set of tools that allow an LLM to control a headless browser using Playwright. It enables navigation, clicking, filling forms, taking screenshots, and extracting text from web pages.

## Tools

### 1. `navigate`
- **Description**: Navigate the browser to a specific URL
- **Parameters**:
  - `url` (string): The URL to navigate to
- **Example**: `navigate({"url": "https://example.com"})`

### 2. `click`
- **Description**: Click on an element identified by a CSS selector
- **Parameters**:
  - `selector` (string): CSS selector of the element to click
- **Example**: `click({"selector": "#submit-button"})`

### 3. `fill`
- **Description**: Fill an input field with text using a CSS selector
- **Parameters**:
  - `selector` (string): CSS selector of the input field
  - `text` (string): Text to fill into the input field
- **Example**: `fill({"selector": "#email-input", "text": "user@example.com"})`

### 4. `screenshot`
- **Description**: Take a screenshot of the current page and return it as base64
- **Parameters**:
  - `path` (string, optional): Path to save the screenshot
- **Example**: `screenshot({"path": "/tmp/screenshot.png"})`

### 5. `get_text`
- **Description**: Extract text content from an element identified by CSS selector
- **Parameters**:
  - `selector` (string): CSS selector of the element to extract text from
- **Example**: `get_text({"selector": "h1"})`

## Requirements

- Node.js >= 18
- Playwright browsers (automatically installed)

## Setup

1. Install dependencies:
```bash
npm install
```

2. Build the project:
```bash
npm run build
```

## Running

To run the agent:

```bash
npm start
```

The agent will communicate via stdio using the MCP protocol.

## Environment Variables

No environment variables required for basic operation. The agent will automatically download and use Playwright browsers.

## Usage with MCP Client

This agent can be used with any MCP-compatible client. The server will listen on stdio and respond to tool calls according to the MCP specification.

## License

MIT
