from fastapi import FastAPI, HTTPException, APIRouter
from models import Product, Order
from helpers import initDB
from bson import ObjectId
from datetime import datetime

router = APIRouter()
db = initDB()


@router.post("/order")
async def create_order(order: Order):
    order_dict = order.dict()
    new_item_list = []
    total_amount = 0
    print(order_dict)
    for item in list(order_dict['items']):
        print(item)
        insert_dict = {
            "product_id": ObjectId(item["product_id"]),
            "quantity": item["quantity"]
        }
        product_item = dict(db.products.find({"_id": ObjectId(item["product_id"])}))
        print(product_item)
        total_amount = total_amount + (product_item["quantity"]*product_item["price"])
        new_item_list.append(insert_dict)
    
    insertQuery = {
        "timestamp": datetime.now(),
        "items": new_item_list,
        "total_amount": total_amount,
        "address": order_dict.address
    }

    result = db.orders.insert_one(insertQuery)
    if result.acknowledged:
        order_id = result.inserted_id
        return {"message": "Placed order", "order_id": str(order_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to placed order")
    
