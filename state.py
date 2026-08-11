from typing import TypedDict

class AgentState(TypedDict):
    user_query: str
    permissions: str
    db_schema : str
    tool_call: list[dict] = []
    tool_result: list[dict] = []
    validation: dict
    result: str
