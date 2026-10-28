# Notion Knowledge Agent

A Q&A agent that can search Notion pages, read their content, and append new content to pages using OpenAI function calling.

## Overview

This agent allows users to interact with their Notion workspace through natural language queries. It can search for pages, read page content, and append new blocks to existing pages.

## Tools

### 1. `search_pages`
Search for Notion pages by title or content.

**Parameters:**
- `query` (string): Search query string
- `limit` (number, optional): Maximum number of results to return (default: 10)

### 2. `read_page`
Read the content of a Notion page.

**Parameters:**
- `page_id` (string): The Notion page ID to read

### 3. `append_block`
Append a new block to the end of a Notion page.

**Parameters:**
- `page_id` (string): The Notion page ID to append to
- `block_content` (string): The content to append as a new block
- `block_type` (enum, optional): The type of block to create (default: paragraph)

## Required Environment Variables

Create a `.env` file with the following variables:

```env
NOTION_TOKEN=your_notion_integration_token
```

You can get a Notion integration token by:
1. Creating a new integration in your Notion workspace
2. Granting it access to the pages you want to query
3. Copying the integration token

## How to Run

1. Install dependencies:
```bash
npm install
```

2. Set up your environment variables in `.env` file

3. Run the agent:
```bash
npm start "Your question here"
```

Example usage:
```bash
npm start "Find all pages about TypeScript"
npm start "Read the content of page abc123"
npm start "Add a note about project deadlines to page xyz789"
```

## Requirements

- Node.js 16+
- Notion integration token with appropriate permissions
- OpenAI API key (configured via environment variables)
- Notion workspace with pages to query
