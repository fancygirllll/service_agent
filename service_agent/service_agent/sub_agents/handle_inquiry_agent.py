from google.adk.agents import Agent

from . import handle_inquiry_agent_prompt
from .. import MODEL
from ..tools.knowledge_inter import knowledge_inter_tool
from ..tools.knowledge_base import knowledge_base_tool
from ..tools.store_state import store_state_tool

HandleInquiryAgent = Agent(
    model = MODEL, 
    name = 'handle_inquiry_agent',
    description = 'Handling user inquiry.',
    instruction = handle_inquiry_agent_prompt.PROMPT,
    tools = [store_state_tool,knowledge_base_tool,knowledge_inter_tool]
)