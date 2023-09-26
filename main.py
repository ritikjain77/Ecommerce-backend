from fastapi import FastAPI
from helpers import initDB  # Import the initDB function from the helpers module
import uvicorn
from api import products, orders  # Import the routers for products and orders

# Create a FastAPI instance
app = FastAPI()

# Initialize the database using the initDB function
db = initDB()

# Include the product and order routers in the FastAPI app
app.include_router(products.router)  # Include the products router
app.include_router(orders.router)    # Include the orders router

# Run the FastAPI app using UVicorn when this script is executed
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the app on host 0.0.0.0 and port 8000