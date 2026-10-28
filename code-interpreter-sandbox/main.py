import os
import sys
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools import load_csv, execute_python, save_chart

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Define system prompt
SYSTEM = """
You are a data analysis agent that helps users analyze CSV data.
You have access to three tools:
1. load_csv: Load a CSV file and get metadata
2. execute_python: Execute Python code to analyze data and generate charts
3. save_chart: Save generated charts to files

When users ask for analysis, use these tools in sequence:
1. First, use load_csv to load their data
2. Then, use execute_python to perform analysis and generate charts
3. Finally, use save_chart to save any charts

Always respond in a clear, structured way with explanations and visualizations.
"""

def main():
    # Get OpenAI API key from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    # Create the agent with tools
    tools = [load_csv, execute_python, save_chart]
    agent = create_react_agent(
        ChatOpenAI(model="gpt-4.1", temperature=0),
        tools,
        prompt=SYSTEM
    )
    
    # Example usage
    print("Code Interpreter Sandbox Agent")
    print("Type 'quit' to exit")
    
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
            messages = result.get("messages", [])
            if messages:
                print(messages[-1].content)
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
