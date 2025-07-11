from google.adk.agents import Agent

from . import MODEL
from .sub_agents.handle_complaint_agent import HandleComplaintAgent
from .sub_agents.handle_inquiry_agent import HandleInquiryAgent
from .sub_agents.handle_general_query_agent import HandleGeneralQueryAgent
from . import root_agent_prompt
from .tools.store_state import store_state_tool

root_agent  = Agent(
    model = MODEL,
    name = 'root_agent',
    description = (
        '调用对应智能体回答用户问题'
    ),
    instruction = root_agent_prompt.PROMPT,
    tools = [store_state_tool],
    sub_agents = [
        HandleComplaintAgent,
        HandleInquiryAgent,
        HandleGeneralQueryAgent,
    ],
)