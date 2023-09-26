from fastapi import HTTPException, APIRouter, Query
from datetime import datetime
from bson import ObjectId
from helpers import initDB
from models import Product, Order, Address
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

# Create an APIRouter instance
router = APIRouter()

# Initialize the database connection using the initDB function
db = initDB()

# Create an order
@router.post("/order")
async def create_order(order: Order):
    order_dict = order.dict()
    new_item_list = []
    total_amount = 0
    print(order_dict)
    
    for item in order_dict['items']:
        print(item)
        # Find the product by ID in the database
        product_item = db.products.find_one({"_id": ObjectId(item["product_id"])})
        
        if product_item:
            quantity = item["quantity"]
            price = product_item["price"]
            total_amount += quantity * price
            insert_dict = {
                "product_id": ObjectId(item["product_id"]),
                "quantity": quantity
            }
            new_item_list.append(insert_dict)
        else:
            raise HTTPException(status_code=404, detail=f"Product with ID {item['product_id']} not found")
    
    # Convert the address to a dictionary
    address_dict = order.address.dict()
    
    # Create the order document to insert into the database
    insertQuery = {
        "timestamp": datetime.now(),
        "items": new_item_list,
        "total_amount": total_amount,
        "address": address_dict  # Use order.address instead of order_dict['address']
    }

    result = db.orders.insert_one(insertQuery)
    if result.acknowledged:
        order_id = result.inserted_id
        return {"message": "Placed order", "order_id": str(order_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to place the order")

# Get a list of orders with pagination
@router.get("/orders/all")
async def get_orders(limit: int = Query(default=10, description="Number of orders to retrieve per page", ge=1),
                     offset: int = Query(default=0, description="Offset for pagination", ge=0)):
    try:
        cursor = db.orders.find().skip(offset).limit(limit)
        orders = []
        for order in cursor:
            order['_id'] = str(order['_id'])
            if 'items' in order:
                for item in order['items']:
                    item['product_id'] = str(item['product_id'])
            orders.append(order)
    
        return {"metaData":{"totalDocuments": len(orders)},"data":orders}
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch orders from the database")

# Get a specific order by ID
@router.get("/order/{orderId}")
async def get_order(orderId: str):
    try:
        order_object_id = ObjectId(orderId)
        order = db.orders.find_one({"_id": order_object_id})

        if order:
            order['_id'] = str(order['_id'])
            if order['items']:
                for item in order['items']:
                    item['product_id'] = str(item['product_id'])
            return {"data": order}
        else:
            raise HTTPException(status_code=404, detail="Order not found")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid order ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch order from the database")
