from typing import Callable, List, Dict, Any, Optional
from pydantic import BaseModel
from openai import OpenAI
import json
import logging
from src.settings import settings

logger = logging.getLogger(__name__)

class Agent(BaseModel):
    name: str
    instructions: str
    model: str = settings.worker_model
    tools: List[Callable] = []
    
    class Config:
        arbitrary_types_allowed = True

class SwarmClient:
    """
    A lightweight implementation of the agent handoff pattern.
    """
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url
        )
        
    def _execute_tool(self, tool_call, tools_map: Dict[str, Callable]) -> str:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        
        logger.info(f"Executing tool: {name}")
        
        if name not in tools_map:
            return f"Error: Tool {name} not found."
            
        func = tools_map[name]
        try:
            result = func(**args)
            
            # If the tool returns another Agent, this is a handoff!
            if isinstance(result, Agent):
                return result
                
            return str(result)
        except Exception as e:
            return f"Error executing tool {name}: {str(e)}"

    def run(self, agent: Agent, messages: List[Dict[str, str]], max_turns: int = 10) -> Dict[str, Any]:
        """Runs the agent loop, handling tool calls and handoffs."""
        current_agent = agent
        history = list(messages)
        
        for _ in range(max_turns):
            # Create a map of tool names to actual python functions
            tools_map = {f.__name__: f for f in current_agent.tools}
            
            # Convert python functions to OpenAI tool schemas
            oai_tools = []
            for f in current_agent.tools:
                # Naive conversion for demo - in prod use Pydantic or docstring parsers
                import inspect
                sig = inspect.signature(f)
                properties = {}
                required = []
                for param_name, param in sig.parameters.items():
                    if param_name == "self": continue
                    properties[param_name] = {"type": "string"}
                    if param.default == inspect.Parameter.empty:
                        required.append(param_name)
                        
                oai_tools.append({
                    "type": "function",
                    "function": {
                        "name": f.__name__,
                        "description": f.__doc__ or f"Execute {f.__name__}",
                        "parameters": {
                            "type": "object",
                            "properties": properties,
                            "required": required
                        }
                    }
                })
            
            logger.info(f"Calling {current_agent.name}...")
            
            # Prep messages with current agent's instructions
            sys_msg = {"role": "system", "content": current_agent.instructions}
            call_messages = [sys_msg] + history
            
            kwargs = {
                "model": current_agent.model,
                "messages": call_messages
            }
            if oai_tools:
                kwargs["tools"] = oai_tools
                
            response = self.client.chat.completions.create(**kwargs)
            message = response.choices[0].message
            history.append(message.model_dump(exclude_none=True))
            
            if not message.tool_calls:
                # The agent provided a final textual response
                return {
                    "messages": history,
                    "agent": current_agent,
                    "content": message.content
                }
                
            # Handle tool calls
            for tool_call in message.tool_calls:
                result = self._execute_tool(tool_call, tools_map)
                
                # Check for Handoff
                if isinstance(result, Agent):
                    logger.info(f"Handoff triggered! {current_agent.name} -> {result.name}")
                    current_agent = result
                    history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": f"Successfully handed off to {result.name}"
                    })
                else:
                    history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
                    
        return {
            "messages": history,
            "agent": current_agent,
            "content": "Error: Reached maximum turns."
        }
