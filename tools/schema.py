from database.model import Products
from langchain_core.tools import tool

from guardrails.validator import toolCallValidation
from pydantic import BaseModel, Field

class schemaCommand(BaseModel):
    table_name : str = Field(min_length=1)
    columns: list[str] = Field(min_length=1, default_factory=list)

@tool
def get_schema(table_name: str) -> dict:
    """Returns a schema of a specified table

    Args:
        table_name(str): name of a table

    Returns:
        list[str]: a list of all the columns of the table
    """
    toolCallValidation(table_name)
    
    # Get the schema of the Products table
    schema = Products.__table__.columns.keys()
    
    print(f"Schema tool result: {schema}")
    
    return schemaCommand(
        table_name=table_name,
        columns=schema
    ) 




get_schema_tool = {
  'type': 'function',
  'function': {
    'name': 'get_schema',
    'description': 'Gets the schema of the Products table.',
    "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        },
  },
}


