# Web Research Crawler

A CrewAI-powered research agent that searches the web, fetches and cleans pages, and writes a cited markdown report to disk.

## Overview

This agent automates the research process by:
1. Searching the web for relevant information
2. Fetching and cleaning content from web pages
3. Writing a comprehensive, cited markdown report to disk

## Tools

### 1. Web Search
- **Purpose**: Search the web for information related to a query
- **Parameters**: `query` (str) - The search query string
- **Returns**: Formatted search results in markdown

### 2. Fetch URL
- **Purpose**: Fetch and clean content from a URL
- **Parameters**: `url` (str) - The URL to fetch content from
- **Returns**: Cleaned text content from the URL

### 3. Write Report
- **Purpose**: Write a cited markdown report to disk
- **Parameters**: 
  - `topic` (str) - The research topic
  - `content` (str) - The main content of the report
  - `sources` (List[Dict[str, str]]) - List of source dictionaries with 'url' and 'title' keys
- **Returns**: Path to the written report file

## Required Environment Variables

Create a `.env` file with the following variables:
```
# No specific environment variables required for this implementation
```

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the agent:
```bash
python main.py
```

The agent will create a report in the `reports/` directory with a filename based on the research topic.

## Example Output

The agent will generate a markdown report like:
```markdown
# Research Report: Artificial Intelligence in Healthcare

Artificial intelligence is revolutionizing healthcare by improving diagnostics, treatment planning, and patient outcomes...

## Sources

1. [AI in Medicine - Nature](https://www.nature.com/articles/s41591-020-01005-3)
2. [Healthcare AI Applications - MIT](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7224027/)
```

## Features

- Web search using DuckDuckGo
- Content cleaning and extraction
- Markdown report generation with citations
- Automatic report saving to disk
- Error handling and timeouts
- Configurable content limits
