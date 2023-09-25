from fastapi import FastAPI, Depends
from helpers import initDB
import uvicorn
from api import products, orders

app = FastAPI()

db = initDB()


app.include_router(products.router)
app.include_router(orders.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




