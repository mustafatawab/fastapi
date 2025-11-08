from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

@app.get("/items/{item_id}")
def get_item(item_id: int):
    """ Get an item by id using path parameters """
    if item_id > 100:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id" : item_id }

@app.get("/items")
def limited_items(limit: int):
    """ Get limited items using query paramters """
    return {"limit" : limit}

class Item(BaseModel):
    name: str
    price: int
    description: str | None = None



@app.post("/items")
def create_item(item: Item):
    """ Create Items """
    return {"name" : item.name , "price" : item.price}




