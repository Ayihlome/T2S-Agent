from langgraph.graph import StateGraph, START, END
from sqlalchemy import inspect

from database.database import engine
from nodes.toolCalling import callTool
from nodes.consolidate import condense
from nodes.deconstructor import deconstruct
from nodes.reflection import reflect, shouldContinue
from state import AgentState

# I need to inject the DB Schema into the agent for better token and step usage
def getDBSchema(engine) -> str:
    """Pre-fetches tables and columns into a clean text block."""
    
    inspector = inspect(engine)
    schema = []
    
    for table_name in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        schema.append(f"Table '{table_name}': columns = {columns}")
    
    return "\n".join(schema)

dbSchema = getDBSchema(engine=engine)

builder = StateGraph(AgentState)

builder.add_node("deconstruct", deconstruct)
builder.add_node("call_tool", callTool)
builder.add_node("condense", condense)
builder.add_node("reflect", reflect)

# build graph
builder.add_edge(START, "deconstruct")
builder.add_edge("deconstruct", "call_tool")
builder.add_edge("call_tool", "reflect")
builder.add_conditional_edges("reflect", shouldContinue )
builder.add_edge("condense", END)

graph = builder.compile()

# calling the graph
state={
    "user_query": "What are we selling and for how much?",
        "permissions": "Limited Access",
        "db_schema" : dbSchema,
        "tool_call": [],
        "tool_result": [],
        "validation": {},
        "result": ""
}

config = {"recursion_limit": 10}

result = graph.invoke(state, config=config)
print(' ')
print(result)
print(f"\nFinal Result: {result.get("content")}")