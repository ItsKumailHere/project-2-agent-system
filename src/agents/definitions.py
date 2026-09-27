from src.agents.core import Agent
from src.tools.web_search import search_web
from src.tools.file_tools import save_markdown_report
from src.settings import settings

# 1. Specialist: Research Agent
research_agent = Agent(
    name="Research Agent",
    instructions="""You are a research specialist.
    Use the search_web tool to find information about the topic requested.
    Always summarize your findings clearly so the next agent can use them.""",
    model=settings.worker_model,
    tools=[search_web]
)

# 2. Specialist: Report Agent
report_agent = Agent(
    name="Report Agent",
    instructions="""You are a technical writer.
    Your job is to take raw findings and format them into a well-structured markdown report.
    Use the save_markdown_report tool to save your work to disk when you are finished.""",
    model=settings.worker_model,
    tools=[save_markdown_report]
)

# Handoff tools for the Orchestrator
def transfer_to_researcher():
    """Call this tool to hand off the conversation to the Research Agent."""
    return research_agent

def transfer_to_writer():
    """Call this tool to hand off the conversation to the Report Agent."""
    return report_agent

# 3. Orchestrator: Triage Agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="""You are the Orchestrator. 
    Analyze the user's request and delegate it to the appropriate specialist:
    - If the user needs information found or researched, use transfer_to_researcher.
    - If the user needs findings formatted and saved to a document, use transfer_to_writer.
    
    You do NOT do the work yourself. You only delegate.""",
    model=settings.orchestrator_model,
    tools=[transfer_to_researcher, transfer_to_writer]
)
