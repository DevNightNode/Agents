import os
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    Runner,
    input_guardrail,
)
from tools import search_flights, search_hotels, book_flight, book_hotel

SENSITIVE_KEYWORDS = ["password", "secret", "token", "credit card", "card number", "ssn"]


@input_guardrail
async def no_sensitive_data(ctx, agent, user_input) -> GuardrailFunctionOutput:
    """Refuse requests that paste secrets or card data into the chat."""
    text = user_input if isinstance(user_input, str) else str(user_input)
    hit = next((k for k in SENSITIVE_KEYWORDS if k in text.lower()), None)
    return GuardrailFunctionOutput(output_info={"matched": hit}, tripwire_triggered=hit is not None)


# Triage agent that determines whether to search flights or hotels
triage_agent = Agent(
    name="Travel Triage Agent",
    instructions="""
    You are a travel planning assistant that helps users plan their trips.
    Your job is to determine if the user wants to book flights or hotels.
    If they want to book flights, hand off to the flight agent.
    If they want to book hotels, hand off to the hotel agent.
    If they want to search for both, ask which they want to do first.
    If they want to do something else, explain that you can only help with flights and hotels.
    """,
    model="gpt-4.1",
    tools=[search_flights, search_hotels],
    input_guardrails=[no_sensitive_data],
    handoffs=[
        Agent(
            name="Flight Agent",
            instructions="""
            You are a flight booking specialist. Help users search for and book flights.
            Use the search_flights tool to find flights, then book_flight to book them.
            """,
            model="gpt-4.1",
            tools=[search_flights, book_flight]
        ),
        Agent(
            name="Hotel Agent",
            instructions="""
            You are a hotel booking specialist. Help users search for and book hotels.
            Use the search_hotels tool to find hotels, then book_hotel to book them.
            """,
            model="gpt-4.1",
            tools=[search_hotels, book_hotel]
        )
    ]
)

def main():
    print("Welcome to OpenAI Travel Planner!")
    print("I can help you search and book flights and hotels.")
    print("Type 'quit' to exit.")
    
    while True:
        user_input = input("\nWhat would you like to do? ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            break
            
        try:
            result = Runner.run_sync(triage_agent, user_input, max_turns=10)
            print("\n" + result.final_output)
        except InputGuardrailTripwireTriggered:
            print("Please don't share passwords or card details here. Try again without them.")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
