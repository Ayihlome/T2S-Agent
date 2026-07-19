from tools.schema import get_schema, get_schema_tool
from tools.list_tables import list_tables, list_tables_tool
from tools.execute_sql import execute_sql, execute_sql_tool
from tools.describe_table import describe_table, describe_table_tool


class ToolManager:
    def __init__(self):
        self.registry = {
            "execute_sql": execute_sql,
            "get_schema": get_schema,
            "list_tables": list_tables,
            "describe_table": describe_table
        }
        self.avaliableTools: list[dict] = [get_schema_tool, list_tables_tool, execute_sql_tool, describe_table_tool]

    
    def callTool(self, tool_request: dict) -> dict:
        if tool_request["tool"] in self.registry:
            tool: function = self.registry.get(tool_request["tool"]) 
            agruments = tool_request["arguments"]

            output = tool(agruments)

            # Returning a dict to feed straight into context

            return {
            "role":"user",
                "content":
            f"""
            Tool {tool_request['tool']} returned:

            {output}

            If this fully answers the question,
            answer the user directly.

            Only call another tool if more information is needed.
            """
        }


