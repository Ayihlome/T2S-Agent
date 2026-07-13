from sqlachemy import Session
from database import engine
from model import Products


def list_tables():
    with Session(engine) as session:
        tables = session.execute("SHOW TABLES")
        return tables.fetchall()
    
