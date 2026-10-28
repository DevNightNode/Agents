import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools import list_tables, describe_table, run_sql_query

# Load environment variables
load_dotenv()

# Define system prompt
SYSTEM = """
You are a SQL analytics assistant that helps users query a PostgreSQL database.
You have access to three tools:
1. list_tables - Lists all tables in the database
2. describe_table - Describes the schema of a specific table
3. run_sql_query - Executes a SQL query and returns results

When users ask for information about tables or schemas, use list_tables and describe_table.
When users want to run queries, use run_sql_query.
Always format your responses clearly and concisely.
If a query returns many rows, summarize the results rather than listing all rows.
"""

def main():
    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4.1", temperature=0)
    
    # Create the agent with tools
    tools = [list_tables, describe_table, run_sql_query]
    agent = create_react_agent(llm, tools, prompt=SYSTEM)
    
    print("SQL Analytics Assistant is ready. Type 'quit' to exit.")
    
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() in ['quit', 'exit']:
                break
                
            result = agent.invoke(
                {"messages": [("user", user_input)]},
                {"recursion_limit": 20}
            )
            
            # Print the final response
            print("\n" + result["messages"][-1].content)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
