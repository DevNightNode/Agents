# MCP Filesystem Server

An MCP server that exposes a project directory to an LLM, allowing it to read, write, list, search, and move files.

## Overview

This agent provides an MCP-compatible server that allows LLMs to interact with a project directory through a set of file system tools. It's designed to be run as a standalone server that can be connected to any MCP-compatible client.

## Tools

### 1. `read_file`
Read the contents of a file.

**Parameters:**
- `file_path` (str): The path to the file to read

**Example:**
```json
{
  "file_path": "src/main.py"
}
```

### 2. `write_file`
Write content to a file.

**Parameters:**
- `file_path` (str): The path to the file to write
- `content` (str): The content to write to the file

**Example:**
```json
{
  "file_path": "docs/README.md",
  "content": "# My Project\n\nThis is a sample project."
}
```

### 3. `list_directory`
List files and directories in a directory.

**Parameters:**
- `directory_path` (str): The path to the directory to list (default: current directory)

**Example:**
```json
{
  "directory_path": "src"
}
```

### 4. `search_files`
Search for files matching a pattern in a directory.

**Parameters:**
- `pattern` (str): The regex pattern to match file names
- `directory_path` (str): The directory to search in (default: current directory)

**Example:**
```json
{
  "pattern": "\\.py$",
  "directory_path": "src"
}
```

### 5. `move_file`
Move a file from source to destination.

**Parameters:**
- `source_path` (str): The path to the source file
- `destination_path` (str): The path to the destination file

**Example:**
```json
{
  "source_path": "temp/file.txt",
  "destination_path": "backup/file.txt"
}
```

## Environment Variables

- `PROJECT_DIR` (required): The absolute path to the project directory that will be exposed to the LLM
- `MCP_SERVER_PORT` (optional): The port to run the server on (default: 8080)

## Running the Agent

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables in a `.env` file:
   ```
   PROJECT_DIR=/path/to/your/project
   ```

3. Run the server:
   ```
   python main.py
   ```

## Security Notes

- The server prevents directory traversal attacks by resolving all paths relative to the configured `PROJECT_DIR`
- All file operations are restricted to the specified project directory
- File paths are validated to ensure they don't escape the project directory

## Usage with MCP Clients

The server can be connected to any MCP-compatible client. The server will expose the following tools:
- `read_file`
- `write_file`
- `list_directory`
- `search_files`
- `move_file`

The server will listen on the port specified by `MCP_SERVER_PORT` (or 8080 by default) and will respond to MCP protocol messages.
