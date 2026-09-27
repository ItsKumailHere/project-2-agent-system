import logging
from src.agents.core import SwarmClient
from src.agents.definitions import triage_agent
from rich.console import Console

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
console = Console()

def run_demo():
    client = SwarmClient()
    
    console.print("[bold green]Starting Multi-Agent Research Demo[/bold green]")
    console.print(f"Orchestrator: [bold]{triage_agent.name}[/bold]")
    
    user_prompt = "Can you research the latest developments in solid state batteries for EVs, and then save a report on it?"
    
    console.print(f"\n[bold blue]User:[/bold blue] {user_prompt}\n")
    
    # Run the swarm
    result = client.run(
        agent=triage_agent,
        messages=[{"role": "user", "content": user_prompt}]
    )
    
    # We loop because the workflow requires multiple passes:
    # Pass 1: User -> Triage -> Handoff to Researcher
    # Pass 2: Researcher (does search) -> Returns text
    # Pass 3: We need to feed the text back to Triage so it can handoff to Writer!
    
    console.print(f"\n[bold yellow]Final Agent:[/bold yellow] {result['agent'].name}")
    console.print(f"[bold green]Output:[/bold green]\n{result['content']}")
    
    # If the researcher did the work but it's not saved yet, we prompt again to save
    if result['agent'].name == "Research Agent":
        console.print("\n[bold magenta]Automatically routing to Report Agent to save findings...[/bold magenta]")
        
        # We start a new turn with the Triage agent, giving it the history
        history = result['messages']
        history.append({"role": "user", "content": "Great, now please format those findings and save them as a report."})
        
        final_result = client.run(
            agent=triage_agent,
            messages=history
        )
        
        console.print(f"\n[bold yellow]Final Agent:[/bold yellow] {final_result['agent'].name}")
        console.print(f"[bold green]Output:[/bold green]\n{final_result['content']}")

if __name__ == "__main__":
    run_demo()
