from pydantic import BaseModel, Field

from inference import model
from guardrails.validator import toolCallValidation
from state import AgentState
from tools.execute_sql import execute_sql
from tools.list_tables import list_tables
from tools.schema import get_schema 

class SQLRequest(BaseModel):
    command : str = Field(description="SQL command to be performed on database")

model_structured = model.with_structured_output(SQLRequest)

tool_register = {
    "execute_sql": execute_sql,
    "get_schema": get_schema,
    "list_tables": list_tables
}

def callTool(state: AgentState):
    toolsState = state.get("tool_call")
    tool_call = toolsState[-1] if toolsState else None      #in case there tool_call is empty
    user_query = state["user_query"]
    
    prompt =f"You are an expert database engineer assistant. Convert this user question into a SQL query: {user_query}"
    
    print(f"Calling tool...({tool_call})")
    command: SQLRequest = model_structured.invoke(prompt)
    
    print("Validating tool call...")
    toolCallValidation(command)
    
    tool = tool_register.get(tool_call["name"])
    
    if not tool:
        raise ValueError("Function not found")
    
    if tool_call["name"] == "list_tables":
        result = tool.invoke({}) #no args
    if tool_call["name"] == "execute_sql":
        result = tool.invoke(tool_call["args"])
    if tool_call["name"] == "get_schema":
        result =tool.invoke(tool_call["args"])
    
    print(f"\nTool Call Node result: {result}")
    
    state["tool_result"].append(result)
    return state
