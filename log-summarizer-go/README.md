# Log Summarizer Go

A Go MCP server that tails log files, identifies error clusters, and posts summaries to a webhook.

## Overview

This agent provides two tools:
1. `read_logs` - Reads the last N lines from a specified log file
2. `post_webhook` - Posts a summary to a specified webhook URL

## Tools

### read_logs
Reads the last N lines from a log file.

**Parameters:**
- `log_path` (string, required): Path to the log file
- `lines` (string, required): Number of lines to read from the end of the file

**Example usage:**
