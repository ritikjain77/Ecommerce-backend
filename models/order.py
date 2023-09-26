from pydantic import BaseModel

# Import the Product model from a separate module
from .product import Product

# Import the datetime module
from datetime import datetime

# Define a Pydantic BaseModel for representing an Item
class Item(BaseModel):
    product_id: str  # ID of the product (string)
    quantity: int    # Quantity of the product (integer)

# Define a Pydantic BaseModel for representing an Address
class Address(BaseModel):
    city: str       # City name (string)
    country: str    # Country name (string)
    zipcode: str    # Zipcode (string)

# Define a Pydantic BaseModel for representing an Order
class Order(BaseModel):
    items: list[Item]  # List of items in the order (a list of Item objects)
    address: Address   # Shipping address for the order (an Address object)
