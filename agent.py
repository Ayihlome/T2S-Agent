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

log.startSession()
# build context
context = ContextBuilder()

prompt = "How much will I make if I sell all the BBQ Lays I have?"
log.conversation.prompt = prompt
context.add_to_history(prompt)
print("Thinking....")


response = llm.generate(prompt=context.build_context(), tools=toolManager.avaliableTools)
log.metrics.prompt_tokens += context.tokenizer(context.history)
log.metrics.completion_tokens += context.tokenizer(response.message.content)

while True:
    try:
        tool_request = json.loads(response.message.content)
        print("Tool being called...")

        log.start_tool(tool_request)
        result: dict = toolManager.callTool(tool_request=tool_request)
        log.finish_tool(result)

        # Add the result to the context and wait for final response, starting with the assistents response
        context.add_to_history({
            "role":"assistant",
            "content": response.message.content
        })

        context.add_to_history(result)

        # Log context after tool call
        ctx = context.build_context()
        log.metrics.prompt_tokens += context.tokenizer(context.history)

        # Second LLM call with tool results
        response = llm.generate(prompt=ctx, tools=toolManager.avaliableTools)

        log.metrics.completion_tokens += context.tokenizer(response.message.content)
        log.llm(response.message.content)

    except json.JSONDecodeError:
        # The resonse now is no longer a JSON so is a response
        print(f"\n Final Response \nUser: {prompt}\nAgent: {response.message.content}")
        log.endSession()
        log.context(context.history)
        log.saveLog() #to a file
        break
        
