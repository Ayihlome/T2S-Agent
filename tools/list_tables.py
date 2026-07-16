from sqlalchemy.orm import Session
from database.database import engine


def list_tables() -> list[dict]:
    """
    Lists all tables in the database and returns them as a list of dictionaries.
    Arguments:
        None
    Returns:
        list[dict]: A list of dictionaries representing the tables in the database.
    """


    with Session(engine) as session:
        tables = session.execute("SHOW TABLES")
        return [dict(table._mapping) for table in tables.fetchall()]
    
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
