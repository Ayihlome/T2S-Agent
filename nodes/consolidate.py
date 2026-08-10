from langchain_ollama import ChatOllama

from state import AgentState

model = ChatOllama(
    model="gemma4:e2b",
    temperature=0
)

def condense(state: AgentState):
    user_query = state["user_query"]
    tool_result = state["tool_result"]
    
    prompt = f"You are a data analyst assistant. Based on this user question: '{user_query}' and the following data retrieved from the database: {tool_result}. Answer the user question in a clear explanation. "
    
    print("Finalizing response...")
    result = model.invoke(prompt)
    
    state["result"] = result
    return state