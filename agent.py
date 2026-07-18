import json
from inference import InferenceEngine
# from tools.list_tables import list_tables, list_tables_tool
# from tools.schema import get_schema, get_schema_tool
# from tools.execute_sql import execute_sql, execute_sql_tool
from contextBuilder.context_manager import ContextBuilder
from tools.ToolManager import ToolManager
from logger.AgentLogging import AgentLogger


llm = InferenceEngine()
toolManager = ToolManager() 
log = AgentLogger()

llm.loadModel(model_name="gemma4:e2b")

# build context
context = ContextBuilder()

prompt = "How many drinks do we currently have in stock?"
context.add_to_history(prompt)


response = llm.generate(prompt=context.build_context(), tools=toolManager.avaliableTools)
log.llm(response.message.content)
print("Thinking....")

while True:
    try:
        tool_request = json.loads(response.message.content)
        print("Tool being called: ", tool_request)

        result: dict = toolManager.callTool(tool_request=tool_request)

        # Add the result to the context and wait for final response, starting with the assistents response
        context.add_to_history({
            "role":"assistant",
            "content": response.message.content
        })

        context.add_to_history(result)

        # Log context after tool call
        ctx = context.build_context()
        log.context(window=ctx)

        response = llm.generate(prompt=ctx, tools=toolManager.avaliableTools)
        log.llm(response.message.content)
    except json.JSONDecodeError:
        # The resonse now is no longer a JSON so is a response
        print(f"\n Final Response \nUser: {prompt}\nAgent: {response.message.content}")
        break
        

print(f"\n Final Response \nUser: {prompt}\nAgent: {response.message.content}")
log.context(context.history)