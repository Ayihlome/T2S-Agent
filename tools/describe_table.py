from sqlalchemy import text
from sqlalchemy.orm import Session
from database.database import engine
from tools.validator import validatePrompt

def describe_table(table_name):
    # Validate the table name
    if not isinstance(table_name, str):
        raise ValueError("Table name must be a string")
    
    with Session(engine) as session:
        # Get the schema of the specified table
        table = session.execute(text(f"PRAGMA table_info({table_name})"))
        return table.fetchall()