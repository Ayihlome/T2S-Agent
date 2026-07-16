from sqlalchemy import text
from sqlalchemy.orm import Session
from database.database import engine
from tools.validator import validatePrompt

def describe_table(table_name) -> list[dict]:
    """
    Gets the schema of a specific table
    Arguments:
        table_name: the name of the table you wish to get the schema of
    Returns:
        list[dict]: a list of dictionaries representing the table 

    """

    # Validate the table name
    if not isinstance(table_name, str):
        raise ValueError("Table name must be a string")
    
    with Session(engine) as session:
        # Get the schema of the specified table
        table = session.execute(text(f"PRAGMA table_info({table_name})"))
        return [dict(coloumn._mapping) for coloumn in table.fetchall()]

describe_table_tool = {
  'type': 'function',
  'function': {
    'name': 'list_tables',
    'description': 'Gets the schema of a specific table',
    'parameters': {
      'type': 'object',
      'required': ['table_name'],
      'properties': {
        'query': {'type': 'string', 'description': 'the name of the table'},
      },
    },
  },
}