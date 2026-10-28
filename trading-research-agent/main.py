import asyncio
import sys
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.genai import types
from tools import get_quote, get_news, compute_indicators, write_brief

# Load environment variables
load_dotenv()

def main():
    # Create the agent with all tools
    root_agent = LlmAgent(
        name="trading_research_agent",
        model="gemini-2.0-flash",
        instruction="""
You are a trading research agent that helps analyze market data for stock symbols.
You have access to four tools:
1. get_quote - Get latest stock quote
2. get_news - Get recent news articles for a symbol
3. compute_indicators - Compute technical indicators
4. write_brief - Generate a daily market brief

When a user asks for analysis of a stock, use these tools in sequence:
1. Get the quote
2. Get news
3. Compute indicators
4. Write a brief

Always respond with a clear, structured brief that includes price, moving averages,
RSI, MACD, and recent news sentiment.
        """,
        tools=[get_quote, get_news, compute_indicators, write_brief]
    )
    
    # Create runner and a session to hold the conversation
    runner = InMemoryRunner(agent=root_agent, app_name="trading_research_agent")
    session = asyncio.run(
        runner.session_service.create_session(app_name="trading_research_agent", user_id="analyst")
    )

    print("Trading Research Agent is ready. Type 'quit' to exit.")

    while True:
        try:
            user_input = input("\n> ")

            if user_input.lower() in ['quit', 'exit']:
                break

            if not user_input.strip():
                continue

            # Run the agent with user input and print its final answer
            message = types.Content(role="user", parts=[types.Part(text=user_input)])
            for event in runner.run(user_id="analyst", session_id=session.id, new_message=message):
                if event.is_final_response() and event.content and event.content.parts:
                    print(event.content.parts[0].text)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
