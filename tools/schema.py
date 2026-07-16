from sqlalchemy.orm import Session
from database.database import engine
from database.model import Products

def get_schema() -> list[str]:
    """
    Gets the schema of the Products table.
    Arguments:
        None
    Returns:
        list[str]: A list of column names in the Products table.
    """

    with Session(engine) as session:
        # Get the schema of the Products table
        schema = Products.__table__.columns.keys()
        return schema

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
