from google.adk.agents import Agent

from . import handle_complaint_agent_prompt
from .. import MODEL
from ..tools.store_state import store_state_tool
from ..tools.append_complaint import append_complaint_tool


HandleComplaintAgent = Agent(
    model = MODEL,
    name = 'handle_complaint_agent',
    description = 'Handling user complaints.',
    instruction = handle_complaint_agent_prompt.PROMPT,
    tools = [store_state_tool, append_complaint_tool]
)