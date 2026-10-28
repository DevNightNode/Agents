import os
from typing import List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection parameters
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

def list_schemas() -> List[str]:
    """
    List all schemas in the PostgreSQL database.
    
    Returns:
        List of schema names
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT schema_name 
                FROM information_schema.schemata 
                WHERE schema_name NOT IN ('information_schema', 'pg_catalog')
                ORDER BY schema_name;
            """)
            schemas = [row['schema_name'] for row in cursor.fetchall()]
            return schemas
    finally:
        conn.close()

def describe_table(schema_name: str, table_name: str) -> Dict[str, Any]:
    """
    Describe the structure of a table in the PostgreSQL database.
    
    Args:
        schema_name: Name of the schema containing the table
        table_name: Name of the table to describe
        
    Returns:
        Dictionary containing table description including columns and data types
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Get column information
            cursor.execute("""
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ordinal_position;
            """, (schema_name, table_name))
            
            columns = cursor.fetchall()
            
            # Get table comment if exists
            cursor.execute("""
                SELECT obj_description(
                    (SELECT oid FROM pg_class WHERE relname = %s AND relnamespace = (
                        SELECT oid FROM pg_namespace WHERE nspname = %s
                    ))
                ) as comment;
            """, (table_name, schema_name))
            
            comment = cursor.fetchone()
            
            return {
                "schema_name": schema_name,
                "table_name": table_name,
                "columns": [
                    {
                        "name": col['column_name'],
                        "type": col['data_type'],
                        "nullable": col['is_nullable'] == 'YES',
                        "default": col['column_default']
                    } for col in columns
                ],
                "comment": comment['comment'] if comment and comment['comment'] else None
            }
    finally:
        conn.close()

def query(sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a SQL query on the PostgreSQL database and return results.
    
    Args:
        sql_query: SQL query to execute
        
    Returns:
        List of rows returned by the query, each row as a dictionary
    """
    # Basic security check to prevent destructive operations
    if any(word in sql_query.lower() for word in ['drop', 'delete', 'update', 'insert', 'alter', 'create']):
        raise ValueError("Query contains prohibited operations. Only SELECT queries are allowed.")
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            if cursor.description:  # If there are results
                return [dict(row) for row in cursor.fetchall()]
            else:
                return []
    finally:
        conn.close()
