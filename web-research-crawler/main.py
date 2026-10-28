import sys
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from tools import web_search, fetch_url, write_report

# Load environment variables
load_dotenv()

def main(topic: str):
    # Define the research agent
    researcher = Agent(
        role="Research Analyst",
        goal="Conduct comprehensive web research on any topic, fetch relevant pages, and write a well-cited markdown report",
        backstory="You are a skilled research analyst with expertise in gathering information from the web, cleaning content, and synthesizing it into clear reports.",
        tools=[web_search, fetch_url, write_report],
        max_iter=10,
        allow_delegation=False,
        verbose=True
    )
    
    # Define tasks
    research_task = Task(
        description="Research the topic '{topic}' by performing web searches, fetching relevant pages, and writing a comprehensive report",
        expected_output="A markdown report with cited sources",
        agent=researcher
    )
    
    # Create and run the crew
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential
    )
    
    # Run the research
    result = crew.kickoff(inputs={"topic": topic})
    
    print("\n=== Research Complete ===")
    print(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python main.py "<research topic>"')
        sys.exit(1)
    main(" ".join(sys.argv[1:]))
