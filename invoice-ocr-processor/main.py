import sys
from pydantic_ai import Agent, RunContext
from tools import extract_invoice, match_purchase_order, schedule_payment
from pydantic import BaseModel
from typing import Optional

# Define dependencies class
class Deps(BaseModel):
    pass

# Create the agent with system prompt and tools
agent = Agent(
    "openai:gpt-4.1",
    deps_type=Deps,
    system_prompt="""
    You are an accounts payable assistant that processes invoices. 
    Your job is to:
    1. Extract invoice details from PDFs
    2. Match purchase orders in the ERP system
    3. Schedule payments for valid invoices
    
    When processing an invoice:
    - First use extract_invoice to get the invoice details
    - Then use match_purchase_order to verify the PO exists
    - Finally, use schedule_payment to process the payment
    
    Always return clear, actionable responses.
    """,
    tools=[extract_invoice, match_purchase_order, schedule_payment]
)

# Main entrypoint
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <invoice.pdf> [extra instructions]")
        sys.exit(1)
    query = f"Process the invoice at {sys.argv[1]}. " + " ".join(sys.argv[2:])

    result = agent.run_sync(query, deps=Deps())
    print(result.output)
