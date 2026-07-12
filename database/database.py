from sqlalchemy import create_engine
from model import Base

engine = create_engine(
    "sqlite:///database/inventory.db",
    echo=True
)

Base.metadata.create_all(bind=engine)