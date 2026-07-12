from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase

class Base (DeclarativeBase):
    pass

class Products(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    price = Column(Integer)
    description = Column(String, index=True)
    sales_pm = Column(Integer)
    quantity = Column(Integer)
    supplier = Column(String, index=True)
    