from typing import TypedDict

class AgentState(TypedDict):
    user_query: str
    permissions: str
    tool_register: list[str]
    tool_call: str
    tool_result: object
    validation: bool
    result: str
