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
    if response.message.tool_calls:
        # Native tool call currently has a bug so I will be falling back to a custom tool calling
        print("Tool Call Detected:", response.tool_calls)
        # if there isnt any tool call then the response is just a normal response from the model and we can break the loop

        # Get the tools being called
        for tool in response.message.tool_calls:
            #  ensure the function is there then called it
            if execute_sql := available_tools.get(tool.function.name):
                    print("Calling function: ", tool.function.name)
                    print('Arguments:', tool.function.arguments)
                    output = execute_sql(**tool.function.arguments)
                    print('Function output:', output)
            else:
                    raise ValueError("'Function', tool.function.name, 'not found'")
            
            if get_schema := available_tools.get(tool.function.name):
                    print("Calling function: ", tool.function.name)
                    print('Arguments:', tool.function.arguments)
                    output = get_schema(**tool.function.arguments)
                    print('Function output:', output)
            else:
                    raise ValueError("'Function', tool.function.name, 'not found'")
            
            if list_table := available_tools.get(tool.function.name):
                    print("Calling function: ", tool.function.name)
                    print('Arguments:', tool.function.arguments)
                    output = list_table(**tool.function.arguments)
                    print('Function output:', output)
            else:
                    raise ValueError("'Function', tool.function.name, 'not found'")
            
            
        # Logging for debugging
        print("Before adding tool:")
        print(context.history)

        # Append the tool results to conetx window
        context.add_to_history({
            "role": "tool",
            "content": str(output),
            "tool_name": tool.fucntion.name["tool"],
            
        })

        print("Updated Context History:", context.history)

        # generate final response

        ctx = context.build_context()
        response = llm.generate(prompt=ctx)
    else:

        break


print("Final Response",response)
print("Context History:", context.history)