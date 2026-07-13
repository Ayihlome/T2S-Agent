from sqlalchemy import Session
from database import engine
from model import Products

def get_schema():
    with Session(engine) as session:
        # Get the schema of the Products table
        schema = Products.__table__.columns.keys()
        return schema
     