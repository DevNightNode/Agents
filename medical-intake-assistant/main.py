import os
import sys
from typing import TypedDict, Annotated, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from tools import lookup_patient, get_available_slots, book_appointment

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Define the state
class MedicalIntakeState(MessagesState):
    pass

# Create the LLM with tools
llm = ChatOpenAI(model="gpt-4.1").bind_tools([lookup_patient, get_available_slots, book_appointment])

# Agent node
def agent_node(state: MedicalIntakeState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# Create the graph
graph = StateGraph(MedicalIntakeState)

# Add nodes
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode([lookup_patient, get_available_slots, book_appointment]))

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

# Main entrypoint
if __name__ == "__main__":
    print("Medical Intake Assistant initialized.")
    print("Type 'quit' to exit.")
    
    # Initialize conversation
    messages = [
        SystemMessage(content="You are a medical intake assistant. Your job is to collect patient symptoms, look up patient records, and book appointments. Always ask for patient ID first. Use the available tools to look up patient information, get available slots, and book appointments.")
    ]
    
    while True:
        user_input = input("Patient: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
            
        messages.append(HumanMessage(content=user_input))
        
        # Run the agent
        try:
            response = app.invoke({"messages": messages}, {"recursion_limit": 25})
            # Keep the full history, including tool calls and results
            messages = response["messages"]
            print(f"Assistant: {messages[-1].content}")
        except Exception as e:
            print(f"Error: {e}")
            messages.append(AIMessage(content=f"Sorry, I encountered an error: {e}"))
