import asyncio
import sys
from claude_agent_sdk import create_sdk_mcp_server, ClaudeAgentOptions, ClaudeSDKClient
from tools import query_metrics, get_incident, acknowledge_incident, restart_service

# Create the MCP server with the defined tools
server = create_sdk_mcp_server(
    name="claude-ops-runbook",
    version="1.0.0",
    tools=[query_metrics, get_incident, acknowledge_incident, restart_service]
)

# Define the system prompt for the agent
SYSTEM_PROMPT = """
You are an incident response assistant that helps with operational tasks.
You have access to tools for querying metrics, retrieving incident details,
acknowledging incidents, and restarting services.

When a user asks for help with an incident:
1. First, use get_incident to retrieve the incident details
2. Then, use query_metrics to check relevant metrics
3. If needed, acknowledge the incident using acknowledge_incident
4. Finally, if a service needs to be restarted, use restart_service

Always be cautious when restarting services and confirm with the user before proceeding.
"""

async def main(query_text: str):
    # Configure the agent options
    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={"claude-ops-runbook": server},
        allowed_tools=[
            "mcp__claude-ops-runbook__query_metrics",
            "mcp__claude-ops-runbook__get_incident",
            "mcp__claude-ops-runbook__acknowledge_incident",
            "mcp__claude-ops-runbook__restart_service",
            "Read",
            "Grep"
        ],
        permission_mode="default",
        max_turns=20
    )
    
    # Create the Claude SDK client
    async with ClaudeSDKClient(options=options) as client:
        await client.query(query_text)
        
        # Process responses
        async for message in client.receive_response():
            print(message)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python main.py "<what to do, e.g. triage incident PXXXXXX>"')
        sys.exit(1)
    asyncio.run(main(" ".join(sys.argv[1:])))
