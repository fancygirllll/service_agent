from google.adk.agents import Agent

from . import handle_general_query_agent_prompt
from .. import MODEL


HandleGeneralQueryAgent = Agent(
    model = MODEL,
    name = 'handle_general_query_agent',
    description = 'Handling user general query.',
    instruction = handle_general_query_agent_prompt.PROMPT,
)