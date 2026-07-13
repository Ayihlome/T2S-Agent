from ast import arguments
import json
import re

from inference import InferenceEngine
from tools import execute_sql
from tools.list_tables import list_tables
from tools.schema import get_schema
from tools.execute_sql import execute_sql
from contextBuilder.context_manager import ContextBuilder


llm = InferenceEngine()

llm.loadModel(model_name="gemma3:1b")

# Tool Registration
tools = {
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

while True:
        response = llm.generate(prompt=context.build_context())
        print("RAW MODEL RESPONSE", response)

        # Check if the response contains a tool call in JSON format
        match = re.search(r"\{.*\}", response, re.DOTALL)  # Match JSON object in the response

        if match:
            tool_call = json.loads(match.group(0)) 
            print("Tool Call Detected:", tool_call)
            # if there isnt any tool call then the response is just a normal response from the model and we can break the loop
            if tool_call is None:
                print(response)
                break

            tool = tools.get(tool_call.get("tool"))

            if tool is None:
                print(response)
                break

            arguments = tool_call.get("arguments") #get the agruments if needed for the tool call
            print("Arguments:", arguments)

            if not arguments:  # If arguments are None or empty, call the tool without arguments
                result = tool()  # Call the tool without arguments
            else:
                result = tool(arguments)  # Call the tool with arguments

            print("Tool Result:", result)
            print("Before adding tool:")
            print(context.history)
            context.add_to_history({
                "role": "tool",
                "name": tool_call["tool"],
                "content": json.dumps(result)
            })
            print("After adding tool:")
            print(context.history)
            print("Updated Context History:", context.history)

            ctx = context.build_context()

            response = llm.generate(prompt=ctx)


print(response)
print("Context History:", context.history)