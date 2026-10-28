import asyncio
import sys
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    create_sdk_mcp_server,
)
from tools import get_changed_files, post_review, run_linter

async def main(query: str):
    # Create the MCP server with our tools
    server = create_sdk_mcp_server(
        name="code-reviewer",
        version="1.0.0",
        tools=[get_changed_files, post_review, run_linter]
    )
    
    # Configure agent options
    options = ClaudeAgentOptions(
        system_prompt="""
        You are a code reviewer agent. Your job is to analyze code changes and provide 
        constructive feedback. You should:
        
        1. Review changed files for code quality, security, and best practices
        2. Suggest improvements where needed
        3. Identify potential bugs or issues
        4. Follow the project's coding standards
        
        Use the available tools to get information about changed files and run linters.
        """,
        mcp_servers={"code-reviewer": server},
        allowed_tools=[
            "mcp__code-reviewer__get_changed_files",
            "mcp__code-reviewer__post_review", 
            "mcp__code-reviewer__run_linter",
            "Read",
            "Grep",
            "Bash"
        ],
        permission_mode="default",
        max_turns=20
    )
    
    # Create the Claude SDK client
    async with ClaudeSDKClient(options=options) as client:
        await client.query(query)

        # Print Claude's text and tool calls as they stream in
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
                    elif isinstance(block, ToolUseBlock):
                        print(f"[tool] {block.name} {block.input}")
            elif isinstance(message, ResultMessage):
                print(f"Done in {message.num_turns} turns")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <github pull request url>")
        sys.exit(1)
    pr_url = sys.argv[1]
    asyncio.run(main(
        f"Review the changes on the current branch (they are the changes in {pr_url}). "
        f"Run the linter on each changed file, then post your review to {pr_url}."
    ))
