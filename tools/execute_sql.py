from sqlalchemy import text
from sqlalchemy.orm import Session  
from database.database import engine
from langchain_core.tools import tool

from pydantic import BaseModel, Field
from guardrails.validator import  toolCallValidation

@tool
def execute_sql(query: str) -> commandResults:
  """Execute SQL command on database

  Args:
      query (str): the command you wish to perform

  Returns:
      list[dict]: the result of the command in a list form of each row
  """
  # Validate the query before execution
  toolCallValidation(query)

  with Session(engine) as session:
      # safe guards should be added to prevent SQL injection attacks
      result = session.execute(text(query))

      rows= [dict(row._mapping) for row in result.fetchall()]

      return commandResults(
        query=query,
        rows=result
      )

class commandResults(BaseModel):
  query : str = Field(min_length=1)
  rows : list[dict] = Field(min_length=1)



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
