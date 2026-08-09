# Takes a user query and produces one (or more) simple query(s) to perform
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama

from state import AgentState
from guardrails.validator import queryValidation

tools = []

model = ChatOllama(
    model="gemma4:e2b",
    temperature=0
)
model_withTools = model.bind_tools(tools)

# break down query
def deconstruct(state: AgentState):
    user_query = state["user_query"]    
    prompt = f"""
    Analyze this request: '{state['user_query']}'
    Select the appropriate tool ({[tool for tool in state["tool_register"]]}) 
    and construct the command string.
    """
    
    queryValidation(user_query)
    
    result = model_withTools.invoke(prompt)
    
    state["tool_call"] = result
    return state["tool_call"]