import asyncio
import sys
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import tools
sys.path.append(str(Path(__file__).parent))
from tools import ingest_directory, query_index, refresh_index

def main():
    # Create the agent with system instructions and tools
    agent = LlmAgent(
        name="rag_docs_chatbot",
        model="gemini-2.0-flash",
        instruction="""
        You are an intelligent documentation assistant. You help users find information in 
        technical documentation by searching through a vector store of documents.
        
        You have access to three tools:
        1. ingest_directory: Load documentation files from a directory into the vector store
        2. query_index: Search for relevant information in the documentation
        3. refresh_index: Re-ingest documentation files to update the vector store
        
        Always use the appropriate tool when requested. When using query_index, 
        provide citations from the retrieved documents in your response.
        """,
        tools=[ingest_directory, query_index, refresh_index]
    )
    
    runner = InMemoryRunner(agent=agent, app_name="rag_docs_chatbot")
    session = asyncio.run(
        runner.session_service.create_session(app_name="rag_docs_chatbot", user_id="local_user")
    )

    print("RAG Docs Chatbot ready. Ask a question, or ask it to ingest a docs folder. Type 'exit' to quit.")
    while True:
        try:
            question = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            continue
        message = types.Content(role="user", parts=[types.Part(text=question)])
        for event in runner.run(user_id="local_user", session_id=session.id, new_message=message):
            if event.is_final_response() and event.content and event.content.parts:
                print(event.content.parts[0].text)


if __name__ == "__main__":
    main()
