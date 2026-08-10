from sqlalchemy.orm import Session
from sqlalchemy import inspect
from database.database import engine
from langchain_core.tools import tool


@tool
def list_tables() -> list[str]:
    """Returns a list of all tables in the database

    Returns:
        list[dict]: a list of table names 
    """
    
    inspector = inspect(engine)
    
    tables = inspector.get_table_names()
    
    return tables


list_tables_tool = {
  'type': 'function',
  'function': {
    'name': 'list_tables',
    'description': 'Lists all tables in the database and returns them as a list of dictionaries.',
    "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        },
  },
}
