from sqlalchemy import text
from sqlalchemy.orm import Session  
from database.database import engine
from tools.validator import validatePrompt


def execute_sql(query):
    # Validate the query before execution
    validatePrompt(query)

    with Session(engine) as session:
        # safe guards should be added to prevent SQL injection attacks
        result = session.execute(text(query))

        rows= [dict(row._mapping) for row in result.fetchall()]

        return rows