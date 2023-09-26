from fastapi import HTTPException
from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
import certifi

# Print the location of the certificate bundle used for SSL/TLS
print(certifi.where())

# Load environment variables from a .env file
load_dotenv()

# Function to initialize the MongoDB database connection
def initDB():
    try:
        # Get the MongoDB connection credentials from environment variables
        username = os.getenv("DB_USERNAME")
        password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        
        # Construct the MongoDB connection URI with SSL/TLS options
        uri = f"mongodb+srv://{username}:{password}@mycluster.xr6i71w.mongodb.net/{db_name}?retryWrites=true&w=majority&ssl=true&ssl_ca_certs={certifi.where()}"
        
        # Create a MongoDB client instance and ping the deployment to check connectivity
        client = MongoClient(uri)
        client.admin.command('ping') 
        
        # Print a success message if the ping is successful
        print("Pinged your deployment. You successfully connected to MongoDB!")
        
        # Return the MongoDB database instance for the "Ecommerce" database
        return client["Ecommerce"]
    except Exception as e:
        # Print the error and raise an HTTP exception with a 500 status code
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to connect to MongoDB: {str(e)}")
