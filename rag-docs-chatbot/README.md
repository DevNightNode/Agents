# RAG Docs Chatbot

A documentation chatbot that ingests documentation files into a vector store and answers questions with citations.

## Overview

This agent allows users to:
1. Ingest documentation from a directory into a vector store
2. Query the documentation using natural language
3. Refresh the index when documentation changes

The chatbot uses Google's Gemini 2.0 Flash model with Chroma as the vector store for semantic search.

## Tools

### 1. `ingest_directory(directory_path: str, chunk_size: int = 1000, chunk_overlap: int = 200)`
Ingests all text files from a directory into a vector store for semantic search.

**Parameters:**
- `directory_path` (str): Path to the directory containing documentation files
- `chunk_size` (int): Maximum number of characters per chunk (default: 1000)
- `chunk_overlap` (int): Number of characters to overlap between chunks (default: 200)

### 2. `query_index(query: str, k: int = 5)`
Queries the vector store for relevant documents based on a natural language query.

**Parameters:**
- `query` (str): Natural language question to search for
- `k` (int): Number of relevant documents to return (default: 5)

### 3. `refresh_index(directory_path: str, chunk_size: int = 1000, chunk_overlap: int = 200)`
Refreshes the vector store by re-ingesting all text files from a directory.

**Parameters:**
- `directory_path` (str): Path to the directory containing documentation files
- `chunk_size` (int): Maximum number of characters per chunk (default: 1000)
- `chunk_overlap` (int): Number of characters to overlap between chunks (default: 200)

## Required Environment Variables

```env
GOOGLE_API_KEY=your_google_api_key_here
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Google API key in a `.env` file:
```bash
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

3. Run the agent:
```bash
python main.py
```

## Usage

The agent will initialize and be ready for interaction. You can use the tools by sending messages in the format:
- `ingest_directory('/path/to/docs')`
- `query_index('How to setup authentication?')`
- `refresh_index('/path/to/docs')`

The agent will respond with appropriate results and citations from the documentation.
