# MCP Postgres Server

A Model Context Protocol (MCP) server that exposes PostgreSQL database capabilities to LLMs. This agent allows LLMs to list schemas, describe tables, and run read-only queries against a PostgreSQL database.

## Features

- **List Schemas**: Retrieve all available schemas in the database
- **Describe Table**: Get detailed information about table structure including columns, data types, and constraints
- **Run Queries**: Execute SELECT queries to retrieve data from the database

## Tools

### `list_schemas`
Lists all schemas in the PostgreSQL database.

### `describe_table`
Describes the structure of a specific table including column names, data types, nullability, and defaults.

### `query`
Executes a SQL SELECT query and returns the results as a list of dictionaries.

## Requirements

- Python 3.8+
- PostgreSQL database connection
- `mcp==1.9.0`
- `psycopg2-binary==2.9.9`
- `python-dotenv==1.0.1`

## Environment Variables

Create a `.env` file with the following variables:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
```

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

The server will start and listen for MCP connections. Configure your MCP client to connect to this server.

## Security

This agent only allows SELECT queries to prevent destructive operations. It will reject any query containing DROP, DELETE, UPDATE, INSERT, ALTER, or CREATE statements.
