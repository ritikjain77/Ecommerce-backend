from fastapi import HTTPException
from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
import certifi

print(certifi.where())


load_dotenv()


def initDB():
    try:
        username = os.getenv("DB_USERNAME")
        password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        uri = f"mongodb+srv://{username}:{password}@mycluster.xr6i71w.mongodb.net/{db_name}?retryWrites=true&w=majority&ssl=true&ssl_ca_certs={certifi.where()}"

        client = MongoClient(uri)
        client.admin.command('ping') 
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client["Ecommerce"]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to connect to MongoDB: {str(e)}")


    
