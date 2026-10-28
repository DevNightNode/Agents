import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools import search_accounts, log_call, update_opportunity, export_report

# Load environment variables
load_dotenv()

# Define system instructions for the agent
SYSTEM = """
You are a Salesforce CRM assistant that helps sales teams manage their CRM data.
You have access to the following tools:
1. search_accounts: Search for Salesforce accounts by name or industry
2. log_call: Log a call activity for an account
3. update_opportunity: Update an opportunity's stage and related fields
4. export_report: Export a Salesforce report

Always be precise in your responses and follow the tool's parameter requirements.
When using tools, make sure to provide all required parameters.
"""

def main():
    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4.1")
    
    # Create the agent with tools
    tools = [search_accounts, log_call, update_opportunity, export_report]
    agent = create_react_agent(llm, tools, prompt=SYSTEM)
    
    # Example usage
    while True:
        try:
            query = input("Enter your request (or 'quit' to exit): ")
            if query.lower() == 'quit':
                break
            
            result = agent.invoke(
                {"messages": [("user", query)]}, 
                {"recursion_limit": 20}
            )
            print("\nResponse:")
            print(result['messages'][-1].content)
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
