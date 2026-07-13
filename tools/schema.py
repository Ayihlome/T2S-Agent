from sqlalchemy.orm import Session
from database.database import engine
from database.model import Products

def get_schema():
    with Session(engine) as session:
        # Get the schema of the Products table
        schema = Products.__table__.columns.keys()
        return schema
     