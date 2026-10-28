import os
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from tools import list_unread, apply_label, draft_reply, forward_email

class AgentState(MessagesState):
    pass

# Create the agent
llm = ChatOpenAI(model="gpt-4.1").bind_tools([list_unread, apply_label, draft_reply, forward_email])

def agent_node(state: AgentState):
    """Agent node that calls the LLM with tools"""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Build the graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode([list_unread, apply_label, draft_reply, forward_email]))

# Add edges
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

# Compile the graph
app = graph.compile()

if __name__ == "__main__":
    # Example usage
    print("Starting email triage agent...")
    
    # Get initial messages
    initial_messages = [
        {"role": "user", "content": "Please triage my unread emails and apply appropriate labels. If any emails are important, draft replies or forward them."}
    ]
    
    # Run the agent
    try:
        for event in app.stream({"messages": initial_messages}, {"recursion_limit": 25}):
            for value in event.values():
                print(value)
    except Exception as e:
        print(f"Error running agent: {e}")
