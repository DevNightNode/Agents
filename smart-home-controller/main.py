import os
from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings
from tools import get_states, set_light, set_thermostat, unlock_door

# Load environment variables
load_dotenv()

# Define the smart home controller agent
smart_home_agent = Agent(
    name="SmartHomeController",
    instructions="""
    You are a smart home controller agent that can interact with Home Assistant.
    You have access to tools to read sensor states and control lights, thermostats, and door locks.
    Always respond in a clear, concise manner to user requests.
    When a user asks about sensor states, use the get_states tool.
    When a user wants to control devices, use the appropriate tool (set_light, set_thermostat, unlock_door).
    """,
    model="gpt-4.1",
    tools=[get_states, set_light, set_thermostat, unlock_door]
)

if __name__ == "__main__":
    # Run the agent with a sample input
    result = Runner.run_sync(
        smart_home_agent,
        user_input="Get the current states of all sensors and devices",
        max_turns=10
    )
    
    print("Final output:", result.final_output)
