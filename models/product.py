from pydantic import BaseModel

# Define a Pydantic BaseModel for representing a Product
class Product(BaseModel):
    name: str        # Name of the product (string)
    price: float     # Price of the product (float)
    quantity: int    # Quantity of the product (integer)
