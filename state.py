from typing import TypedDict

class AgentState(TypedDict):
    user_query: str
    permissions: str
    tool_call: dict
    tool_result: list[dict]
    validation: bool
    result: str
