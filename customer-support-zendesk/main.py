import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools import search_help_center, get_ticket, reply_to_ticket, escalate_ticket

# System instructions for the agent
SYSTEM = """
You are a customer support agent that helps resolve customer issues using Zendesk.
You have access to four tools:
1. search_help_center - Search the help center for articles related to a query
2. get_ticket - Retrieve a specific ticket by ID
3. reply_to_ticket - Reply to a ticket with a message
4. escalate_ticket - Escalate a ticket by assigning it or changing priority

When responding to a user, you should:
- First use the appropriate tools to gather information
- Then formulate a helpful response
- If a ticket needs to be escalated, use the escalate_ticket tool
- If a ticket needs a reply, use the reply_to_ticket tool
- Always be polite and professional

Remember to use the tools appropriately and never make up information.
"""

def main():
    # Initialize the LLM with GPT-4.1
    llm = ChatOpenAI(model="gpt-4.1", temperature=0)
    
    # Create the agent with the tools
    tools = [
        search_help_center,
        get_ticket,
        reply_to_ticket,
        escalate_ticket
    ]
    
    agent = create_react_agent(llm, tools, prompt=SYSTEM)
    
    # Example usage
    while True:
        try:
            query = input("Enter your query (or 'quit' to exit): ")
            if query.lower() == 'quit':
                break
            
            result = agent.invoke(
                {"messages": [("user", query)]}, 
                {"recursion_limit": 20}
            )
            
            print("\nAgent response:")
            print(result["messages"][-1].content)
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
