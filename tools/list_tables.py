from sqlalchemy.orm import Session
from database.database import engine


def list_tables():
    with Session(engine) as session:
        tables = session.execute("SHOW TABLES")
        return tables.fetchall()
    
