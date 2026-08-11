from pydantic import BaseModel, Field
from typing import Optional, Any
from langchain_core.messages import ToolCall

from state import AgentState
from inference import model

# I need to create a custom tool call to ensure that the AI produces the right output
class ToolCallSpec(BaseModel):
    name : str = Field(description="Name of the tool to execute")
    args : dict[str, Any] =Field(default_factory=dict, description="Arguments for the tool")
class Checkpoint(BaseModel):
    complete : bool = Field(description="True if no more tools are needed to answer the user, False if more tools are needed")
    tool_call : Optional[ToolCallSpec] = Field(         #Optional because it may come back True and no need for too call
        default=None, 
        description="The tool call details, or None if complete is True"
    ) 

model_structured = model.with_structured_output(Checkpoint)

def reflect(state:AgentState):
    user_query = state["user_query"]
    tool_result = state["tool_result"]
    
    prompt =f"You are an expert database engineer assistant. From this users question: '{user_query}' determine if you have enough information to answer their question also based on these previous tool calls: {tool_result}. If you decide you do not have enough information(where complete is false) (missing information such as tables and column names), select the appropriate tool (execute_sql, get_schema, list_tables) and construct the command string."
    
    print("Validating information...")
    result : Checkpoint = model_structured.invoke(prompt)
    
    # return {
    #     "validation": {
    #         "complete": result.complete,
    #         "tool_call": result.tool_call.model_dump() if result.tool_call else None
    #     }
    # }   
    state["validation"] = {
        "complete": result.complete,
        "tool_call":  result.tool_call.model_dump() if result.tool_call else None
    }
    return state

def shouldContinue(state: AgentState):
    # if not state["validation"]["complete"]:
    #     return "call_tool"
    # return "condense"
    if state["validation"]["complete"] == False:
        state["tool_call"].append(state["validation"]["tool_call"])
        return "call_tool"
    else:
        return "condense"