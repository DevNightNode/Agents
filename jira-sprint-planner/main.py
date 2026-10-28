import asyncio
import sys
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from tools import search_issues, create_issue, transition_issue, add_comment

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

async def main(task: str):
    # Create the agent with tools
    agent = AssistantAgent(
        name="SprintPlanner",
        model_client=OpenAIChatCompletionClient(model="gpt-4.1"),
        tools=[search_issues, create_issue, transition_issue, add_comment],
        system_message="""
        You are a Jira Sprint Planning assistant. Your role is to help plan sprints by:
        1. Searching for backlog items
        2. Creating new issues
        3. Transitioning issues through workflows
        4. Adding comments to issues
        
        When asked to plan a sprint:
        - First search for relevant issues in the backlog
        - Estimate effort for stories
        - Create new issues if needed
        - Transition issues to appropriate states
        - Add comments to track planning decisions
        
        Always use the tools provided to interact with Jira.
        """
    )
    
    # Run the agent
    result = await agent.run(task=task)
    print(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python main.py "<planning request, e.g. plan sprint 42 for project WEB from the To Do backlog>"')
        sys.exit(1)
    asyncio.run(main(" ".join(sys.argv[1:])))
