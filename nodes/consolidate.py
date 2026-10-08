from state import AgentState
from inference import model



def condense(state: AgentState):
    user_query = state["user_query"]
    tool_result = state["tool_result"]
    
    prompt = f"You are a data analyst assistant. Based on this user question: '{user_query}' and the following data retrieved from the database: {tool_result[-1]}. Answer the user question in a clear explanation. "
    
    print("Finalizing response...")
    result = model.invoke(prompt)
    
    state["result"] = result
    return state