import os
import sys
from agents import Agent, Runner, ModelSettings
from tools import get_ci_logs, clone_repo, run_tests, apply_patch, open_pull_request

# Environment variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Check for required environment variables
if not GITHUB_TOKEN or not OPENAI_API_KEY:
    print("Error: GITHUB_TOKEN and OPENAI_API_KEY environment variables must be set")
    sys.exit(1)

# System instructions for the agent
AGENT_INSTRUCTIONS = """
You are a CI failure fixing agent. Your job is to:
1. Read CI logs to understand what failed
2. Clone the repository
3. Run tests to reproduce the failure
4. Apply fixes to files
5. Open a pull request with the fix

Always follow these steps:
1. First, get the CI logs
2. Then, clone the repository
3. Run the tests to reproduce the failure
4. Analyze the failure and create a fix
5. Apply the fix to the repository
6. Open a pull request with the fix

Be very careful about the commands you run and the changes you make.
"""

def main():
    # Create the agent with all required tools
    agent = Agent(
        name="ci-failure-fixer",
        instructions=AGENT_INSTRUCTIONS,
        model="gpt-4.1",
        tools=[
            get_ci_logs,
            clone_repo,
            run_tests,
            apply_patch,
            open_pull_request
        ]
    )
    
    if len(sys.argv) != 4:
        print("Usage: python main.py <ci_log_url> <owner/repo> <test_command>")
        sys.exit(1)
    ci_url, repo_full_name, test_command = sys.argv[1:4]
    user_input = (
        f"Please fix this CI failure.\n"
        f"CI log URL: {ci_url}\n"
        f"Repository: https://github.com/{repo_full_name} ({repo_full_name})\n"
        f"Test command: {test_command}"
    )
    
    # Run the agent
    result = Runner.run_sync(agent, user_input, max_turns=10)
    
    print("Final output:")
    print(result.final_output)

if __name__ == "__main__":
    main()
