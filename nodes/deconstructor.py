# Takes a user query and produces one (or more) simple query(s) to perform
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama

from state import AgentState
from guardrails.validator import queryValidation
from tools.execute_sql import execute_sql
from tools.list_tables import list_tables
from tools.schema import get_schema 

tools = [execute_sql, get_schema, list_tables]

model = ChatOllama(
    model="gemma4:e2b",
    temperature=0.2
)
model_withTools = model.bind_tools(tools)

# break down query
def deconstruct(state: AgentState):
    user_query = state["user_query"]    
    prompt = f"""
    Analyze this request: '{state['user_query']}'
    Select the appropriate tool (execute_sql, get_schema, list_tables) 
    and construct the command string.
    """
    
    print("Validating query")
    queryValidation(user_query)
    
    print("Selecting tool...")
    result = model_withTools.invoke(prompt)

    
    print(f"Tool selected: {result}")
    print(f"Tool call: {result.tool_calls[0]}")
    
    
    state["tool_call"] = result.tool_calls[0]
    return state