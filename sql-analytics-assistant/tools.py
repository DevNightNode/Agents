import os
from typing import List, Dict, Any
from langchain_core.tools import tool
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection setup
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    """Create and return a database connection."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )

@tool
def list_tables() -> List[Dict[str, Any]]:
    """
    List all tables in the database.
    
    Returns:
        A list of dictionaries containing table information.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name, table_schema
                FROM information_schema.tables
                WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
                ORDER BY table_schema, table_name;
            """)
            tables = cur.fetchall()
            return [{"name": t["table_name"], "schema": t["table_schema"]} for t in tables]
    finally:
        conn.close()

@tool
def describe_table(table_name: str, schema_name: str = "public") -> Dict[str, Any]:
    """
    Describe the schema of a specific table.
    
    Args:
        table_name (str): Name of the table to describe
        schema_name (str): Name of the schema (default: 'public')
        
    Returns:
        A dictionary containing the table schema information.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Get column information
            cur.execute("""
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = %s
                ORDER BY ordinal_position;
            """, (table_name, schema_name))
            columns = cur.fetchall()
            
            # Get primary key information
            cur.execute("""
                SELECT a.attname
                FROM pg_index i
                JOIN pg_class c ON c.oid = i.indrelid
                JOIN pg_class c2 ON c2.oid = i.indexrelid
                JOIN pg_namespace n ON n.oid = c.relnamespace
                JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = ANY(i.indkey)
                WHERE c.relname = %s AND n.nspname = %s AND i.indoption[0] = 1
            """, (table_name, schema_name))
            primary_keys = [row[0] for row in cur.fetchall()]
            
            return {
                "table_name": table_name,
                "schema_name": schema_name,
                "columns": [
                    {
                        "name": col["column_name"],
                        "type": col["data_type"],
                        "nullable": col["is_nullable"] == "YES",
                        "default": col["column_default"]
                    } for col in columns
                ],
                "primary_keys": primary_keys
            }
    finally:
        conn.close()

@tool
def run_sql_query(query: str) -> Dict[str, Any]:
    """
    Execute a SQL query and return the results.
    
    Args:
        query (str): The SQL query to execute
        
    Returns:
        A dictionary containing the query results and metadata.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            
            # If it's a SELECT query, fetch results
            if query.strip().upper().startswith("SELECT"):
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                return {
                    "query": query,
                    "columns": columns,
                    "rows": [dict(row) for row in rows],
                    "row_count": len(rows)
                }
            else:
                # For non-SELECT queries, return affected rows
                conn.commit()
                return {
                    "query": query,
                    "affected_rows": cur.rowcount,
                    "status": "Query executed successfully"
                }
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
