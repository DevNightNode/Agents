import asyncio
import sys
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from tools import tools

# Load environment variables
load_dotenv()

async def main(task: str):
    # Create the assistant agent with the tools
    agent = AssistantAgent(
        name="security_log_analyst",
        model_client=OpenAIChatCompletionClient(
            model="gpt-4.1"
        ),
        tools=tools,
        system_message="""
        You are a Security Operations Center (SOC) analyst assistant. Your role is to:
        1. Search authentication logs for failed login attempts
        2. Enrich IP addresses with reputation information
        3. Block malicious IPs via firewall
        4. Create security incidents for suspicious activities
        
        When analyzing logs:
        - Look for failed authentication attempts
        - Focus on IP addresses with multiple failed attempts
        - Check reputation of suspicious IPs
        - Block IPs that are flagged as malicious
        - Create incidents for high-risk activities
        
        Always use the tools provided to perform actions. Do not make up responses or perform actions outside of the tools.
        """
    )
    
    
    # Run the agent with the task
    result = await agent.run(task=task)
    
    print("Agent response:")
    print(result)

if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) or (
        "Analyze failed logins from now-1h to now. Look up the reputation of any IP with "
        "5 or more failures, block IPs with an abuse score of 80 or more, and open an incident."
    )
    asyncio.run(main(task))
