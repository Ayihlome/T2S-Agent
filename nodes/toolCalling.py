from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama

from guardrails.validator import toolCallValidation
from state import AgentState
from tools.execute_sql import execute_sql
from tools.list_tables import list_tables
from tools.schema import get_schema 

class SQLRequest(BaseModel):
    command : str = Field(description="SQL command to be performed on database")

model = ChatOllama(
    model="gemma4:e2b",
    temperature=0
)
model_structured = model.with_structured_output(SQLRequest)

tool_register = {
    "execute_sql": execute_sql,
    "get_schema": get_schema,
    "list_tables": list_tables
}

def callTool(state: AgentState):
    tool_call = state["tool_call"]
    user_query = state["user_query"]
    
    prompt =f"You are an expert database engineer assistant. Convert this user question into a SQL query: {user_query}"
    
    command: SQLRequest = model_structured.invoke(prompt)
    
    toolCallValidation(result)
    
    tool = tool_register.get(tool_call)
    
    if not tool:
        raise ValueError("Function not found")
    
    result = tool(command)
    
    state["tool_result"] = result
    return state
