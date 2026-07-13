from sqlalchemy.orm import Session
from database.database import engine
from database.model import Products

with Session(engine) as session:
    prod1 = Products(product_name="Coca Cola 2L", price=18, description="2L Bottle", sales_pm=25, quantity=100, supplier="Coke Man")
    prod2 = Products(product_name="BBQ Lays", price=12, description="BBQ Flavored", sales_pm=17, quantity=200, supplier="Lays Inc.")
    prod3 = Products(product_name="Pepsi 2L", price=18, description="2L Bottle", sales_pm=20, quantity=150, supplier="Pepsi Co.")
    prod4 = Products(product_name="Doritos Nacho Cheese", price=15, description="Nacho Cheese Flavor", sales_pm=22, quantity=180, supplier="Frito-Lay")


    session.add_all([prod1, prod2, prod3, prod4])
    session.commit()

