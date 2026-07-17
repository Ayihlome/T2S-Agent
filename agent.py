from ast import arguments
import json
import re
from inference import InferenceEngine
from tools.list_tables import list_tables, list_tables_tool
from tools.schema import get_schema, get_schema_tool
from tools.execute_sql import execute_sql, execute_sql_tool
from contextBuilder.context_manager import ContextBuilder


llm = InferenceEngine()

llm.loadModel(model_name="gemma4:e2b")

# Tool Registration
available_tools = {
    "execute_sql": execute_sql,
    "get_schema": get_schema,
    "list_tables": list_tables
}

# build context
context = ContextBuilder()

prompt = "What products are we selling?"
context.add_to_history(prompt)

# try:
    
        
# except Exception as e:
#     print(f"An error occurred: {str(e)}")


response = llm.generate(prompt=context.build_context(), tools=[execute_sql_tool, get_schema_tool, list_tables_tool])
print("Thinking....")
print("RAW MODEL RESPONSE", response)

while True:
    try:
        tool_request = json.loads(response.message.content)
        print("Tool being called: ", tool_request)
    except json.JSONDecodeError:
        # The resonse now is no longer a JSON so is a response
        print("\n FINAL RESPONSE (None JSON): ", response.message.content)
        break

    if tool_request["tool"] in available_tools:
        tool : function = available_tools.get(tool_request["tool"])
        output = tool(tool_request["arguments"])

        # Add the result to the context and wait for final response, starting with the assistents response
        context.add_to_history({
            "role":"assistant",
            "content": response.message.content
        })

        context.add_to_history({
            "role":"user",
                "content":
            f"""
            Tool execute_sql returned:

            {output}

            If this fully answers the question,
            answer the user directly.

            Only call another tool if more information is needed.
            """
        })

        print("\n Uploading current context:  ", context.history)
        response = llm.generate(prompt=context.build_context(), tools=[execute_sql_tool, get_schema_tool, list_tables_tool])
        print("\n POST TOOL RESPONSE: ", response )
    else:
        print("Tool not found...")
        break




print("\n Final Response",response)
print("Context History:", context.history)