# SQL Analytics Assistant

A natural language-to-SQL analytics agent that interacts with a PostgreSQL warehouse. This agent helps users explore database schemas, run queries, and understand their data through conversational interactions.

## Features

- **Natural Language Interface**: Convert natural language questions into SQL queries
- **Schema Exploration**: List tables and describe table schemas
- **Query Execution**: Run SQL queries and return structured results
- **Data Summarization**: Automatically summarize large query results

## Tools

### 1. `list_tables`
Lists all tables in the database with their schemas.

**Example usage**: "What tables are available in the database?"

### 2. `describe_table`
Describes the schema of a specific table including column names, data types, and primary keys.

**Example usage**: "Describe the customers table"

### 3. `run_sql_query`
Executes a SQL query and returns the results in a structured format.

**Example usage**: "Show me the first 10 customers"

## Requirements

- Python 3.8+
- PostgreSQL database connection
- OpenAI API key

## Environment Variables

Create a `.env` file with the following variables:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
OPENAI_API_KEY=your_openai_api_key
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variables in `.env` file

3. Run the agent:
```bash
python main.py
```

## Usage

The agent will prompt you for input. You can ask questions like:
- "List all tables"
- "Describe the orders table"
- "Show me the top 5 customers by total orders"
- "What's the average order value?"

The agent will automatically use the appropriate tools to answer your questions and execute SQL queries against your PostgreSQL database.

## Security Notes

- The agent only executes SELECT queries by default (read-only operations)
- All database connections use secure SSL connections
- Environment variables are used for credentials
- Query results are sanitized before being returned to the user
