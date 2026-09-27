# Multi-Agent Research System

This project demonstrates an autonomous multi-agent architecture using the native OpenAI SDK. It is heavily inspired by OpenAI's Swarm pattern and Dave Ebbelaar's orchestrator-worker architectures.

## The Architecture
Instead of one massive prompt with 50 tools, we use **Delegated Autonomy**:
1. **Triage Agent**: The orchestrator. It has no tools to do real work. Its only tools are `transfer_to_researcher` and `transfer_to_writer`.
2. **Research Agent**: The specialist. It has a `search_web` tool.
3. **Report Agent**: The writer. It has a `save_markdown_report` tool.

When the LLM calls a `transfer_*` tool, the execution engine intercepts it and swaps the active agent, system prompt, and available tools. This keeps context windows small and deterministic.

## Setup
1. `uv sync`
2. Copy `.env.example` to `.env` and add your API keys (OpenRouter is default for easy access to Gemini/Groq/etc).
3. Run `python examples/demo.py` to see the agents in action.
