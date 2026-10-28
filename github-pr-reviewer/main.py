import os
import sys
from agents import Agent, Runner, ModelSettings
from tools import get_pull_request_diff, post_review_comment, submit_review

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# System instructions for the agent
AGENT_INSTRUCTIONS = """
You are a GitHub pull request reviewer. Your job is to analyze pull requests and provide feedback.
When a user provides a GitHub owner, repo, and pull request number, you should:
1. Fetch the pull request diff
2. Analyze the changes for potential issues
3. Comment on risky changes if needed
4. Submit a final review (approve or request changes)

Use the available tools to interact with GitHub.
"""

def main():
    # Create the agent with tools
    agent = Agent(
        name="GitHub PR Reviewer",
        instructions=AGENT_INSTRUCTIONS,
        model="gpt-4.1",
        tools=[
            get_pull_request_diff,
            post_review_comment,
            submit_review
        ]
    )
    
    # Get user input
    if len(sys.argv) < 4:
        print("Usage: python main.py <owner> <repo> <pull_number>")
        sys.exit(1)
    
    owner = sys.argv[1]
    repo = sys.argv[2]
    pull_number = int(sys.argv[3])
    
    # Run the agent
    user_input = f"Review pull request #{pull_number} in {owner}/{repo}"
    result = Runner.run_sync(agent, user_input, max_turns=10)
    
    print("Final output:")
    print(result.final_output)

if __name__ == "__main__":
    main()
