# Multi-Agent System Architecture

This project demonstrates the "Orchestrator-Worker" pattern using native Python tool calling.

## Key Patterns
- **Delegated Autonomy**: A central Triage agent receives the user's prompt and decides which specialist agent to hand off to.
- **Agent Handoffs**: Agents are represented as functions that return other Agents. This is the core pattern popularized by OpenAI's Swarm framework.
- **Model Tiering**: The orchestrator uses a highly capable model to plan and delegate. The workers use fast, cheap models since their tasks are narrowly scoped.
- **Guardrails**: Input is filtered before hitting the orchestrator; outputs are validated via Pydantic before returning to the user.

## Agents
1. **Triage Agent**: The orchestrator. Decides routing.
2. **Research Agent**: Has tools to search the web and read documentation.
3. **Report Agent**: Has tools to format and save output as markdown.
