import sys
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from tools import get_pods, get_pod_logs, restart_deployment, scale_deployment

# Load environment variables
load_dotenv()

# Define the DevOps agent
devops_agent = Agent(
    role="Kubernetes DevOps Engineer",
    goal="Inspect Kubernetes workloads, tail pod logs, and perform restart or scaling operations",
    backstory="You are a skilled DevOps engineer with deep knowledge of Kubernetes operations. You can inspect workloads, view logs, and perform restart or scaling operations on deployments.",
    tools=[get_pods, get_pod_logs, restart_deployment, scale_deployment],
    max_iter=10,
    allow_delegation=False
)

# One task per run, driven by the operator's request
ops_task = Task(
    description=(
        "Handle this Kubernetes operations request: {request}. "
        "Inspect the relevant pods and logs before changing anything, and only restart or "
        "scale a deployment when the request asks for it."
    ),
    expected_output="What you inspected, what you changed (if anything), and the resulting state",
    agent=devops_agent
)

# Create the crew
crew = Crew(
    agents=[devops_agent],
    tasks=[ops_task],
    process=Process.sequential
)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python main.py "<request, e.g. why is checkout-api crashlooping in prod?>"')
        sys.exit(1)

    result = crew.kickoff(inputs={"request": " ".join(sys.argv[1:])})
    print(result)
