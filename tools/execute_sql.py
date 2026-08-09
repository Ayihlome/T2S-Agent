from sqlalchemy import text
from sqlalchemy.orm import Session  
from database.database import engine
from tools.validator import validatePrompt


def execute_sql(query: str) -> list[dict]:
    # Validate the query before execution
    validatePrompt(query)

    with Session(engine) as session:
        # safe guards should be added to prevent SQL injection attacks
        result = session.execute(text(query))

        rows= [dict(row._mapping) for row in result.fetchall()]

        return rows

execute_sql_tool = {
  'type': 'function',
  'function': {
    'name': 'execute_sql',
    'description': 'Executes a SQL query against the database and returns the results as a list of dictionaries.',
    'parameters': {
      'type': 'object',
      'required': ['query'],
      'properties': {
        'query': {'type': 'string', 'description': 'The SQL query string to be executed.'},
      },
    },
  },
}
