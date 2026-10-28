import sys
import os
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from tools import create_workspace_user, create_okta_user, add_to_group, send_welcome_email

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Define the agent state
class AgentState(MessagesState):
    pass

# Initialize the LLM with tools
llm = ChatOpenAI(model="gpt-4.1").bind_tools([
    create_workspace_user,
    create_okta_user,
    add_to_group,
    send_welcome_email
])

# Define the agent node
def agent_node(state: AgentState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# Create the graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode([create_workspace_user, create_okta_user, add_to_group, send_welcome_email]))

# Add edges
graph.add_edge(START, "agent")
graph.add_conditional_edges(
    "agent",
    tools_condition,
)
graph.add_edge("tools", "agent")
graph.add_edge("agent", END)

# Compile the graph
app = graph.compile()

# Entry point
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python main.py "<onboarding request, e.g. onboard Jane Doe as a Software Engineer in Engineering>"')
        sys.exit(1)
    messages = [HumanMessage(content=" ".join(sys.argv[1:]))]
    
    try:
        for output in app.stream({"messages": messages}, {"recursion_limit": 25}):
            for key, value in output.items():
                print(f"Output from {key}:")
                print(value)
                print()
    except Exception as e:
        print(f"Error running agent: {e}")
