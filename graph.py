from langgraph.graph import StateGraph, START, END

from nodes.toolCalling import callTool
from nodes.consolidate import condense
from nodes.deconstructor import deconstruct
from nodes.reflection import reflect, shouldContinue
from state import AgentState


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
        "tool_call": [],
        "tool_result": [],
        "validation": {},
        "result": ""
}

config = {"recursion_limit": 10}

result = graph.invoke(state, config=config)
print(' ')
print(result)
print(f"\nFinal Result: {result["result"]}")