# Takes a user query and produces one (or more) simple query(s) to perform
from state import AgentState
from inference import model
from guardrails.validator import queryValidation
from tools.execute_sql import execute_sql
from tools.list_tables import list_tables
from tools.schema import get_schema 

tools = [execute_sql, get_schema, list_tables]

model_withTools = model.bind_tools(tools)

# break down query
def deconstruct(state: AgentState):
    user_query = state["user_query"]    
    dbSchema = state["db_schema"]
    prompt = f"""
    Analyze this request: '{state['user_query']}'
    Select the appropriate tool (execute_sql, get_schema, list_tables) 
    and construct the command string.
    Ensure you have a full understanding of the tables and their schemas before executing SQL commands.
    For context, here is the current database schema, just the name of the tables and the columns in them: {dbSchema}
    """
    
    print("Validating query")
    queryValidation(user_query)
    
    print("Selecting tool...")
    result = model_withTools.invoke(prompt)

    
    print(f"Tool selected: {result}")
    print(f"Tool call: {result.tool_calls[0]}")
    
    
    state["tool_call"].append(result.tool_calls[0])
    return state