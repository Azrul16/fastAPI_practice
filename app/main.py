from fastapi import FastAPI
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: float

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/users/admin")
async def read_admin():
    return {f"I'm admin."}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": f"Your item id is {item_id}"}



@app.get("/products")
async def read_product(id):
    return {"product_id": f"Your product id is {id}"}


@app.post("/addproducts")
async def add_product(product: Product):
    return {"product_id": f"Your product id is {product.id} name is {product.name} and price is {product.price}"}




