from fastapi import APIRouter, HTTPException
from models import Product
from helpers import initDB
from bson import ObjectId


router = APIRouter()
db = initDB()


@router.post('/products')
async def create_product(product: Product):
    result = db.products.insert_one(product.dict())
    print(result)
    if result.acknowledged:
        product_id = result.inserted_id
        return {"message": "Product created", "product_id": str(product_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to create product")


@router.patch('/products/{product_id}')
async def update_product(product_id: str, product: Product):
    filter_query = {"_id": ObjectId(product_id)}
    update_query = {"$set": {"quantity": product.quantity}}
    try:
        result = db.products.update_one(filter_query, update_query)
        if result.modified_count == 1:
            return {"data": "Product updated successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update: {str(e)}")



@router.get('/products/all')
async def fetch_products():
    products = list(db.products.find({}, {"_id": 0}))  
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return {"metaData":{"totalProducts": len(products)},"data":products}






    
    