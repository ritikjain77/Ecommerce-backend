from pydantic import BaseModel
from .product import Product
# import datetime
from datetime import datetime

class Item(BaseModel):
    product_id: str
    quantity: int

class Address(BaseModel):
    city: str
    country: str
    zipcode: str

class Order(BaseModel):
    items: list[Item]
    address: Address