import os
from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings
from tools import list_idle_instances, list_unattached_volumes, stop_instance, delete_volume

# Load environment variables
load_dotenv()

# Define the agent
agent = Agent(
    name="aws-cost-optimizer",
    instructions="""
    You are an AWS cost optimization expert. Your job is to help users identify and 
    optimize AWS resources to reduce costs. You can:
    
    1. List idle EC2 instances that are consuming resources but not being used
    2. List unattached EBS volumes that are wasting storage space
    3. Stop idle EC2 instances to save costs
    4. Delete unattached EBS volumes to save storage costs
    
    When a user asks to optimize resources, first list the idle instances or unattached volumes.
    Then, if the user requests to take action (stop/delete), confirm the action before proceeding.
    Always provide clear explanations of potential savings.
    
    Use the tools provided to interact with AWS resources.
    """,
    model="gpt-4.1",
    tools=[list_idle_instances, list_unattached_volumes, stop_instance, delete_volume]
)

if __name__ == "__main__":
    print("AWS Cost Optimizer Agent")
    print("Type 'quit' to exit")
    
    while True:
        user_input = input("\n> ")
        
        if user_input.lower() in ['quit', 'exit']:
            break
            
        try:
            result = Runner.run_sync(agent, user_input, max_turns=10)
            print(result.final_output)
        except Exception as e:
            print(f"Error: {e}")
