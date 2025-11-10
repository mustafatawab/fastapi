from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float


class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


items : list[Item] = []

next_id = 1

@app.post("/items/", response_model=Item)
def create_item(item: ItemCreate):
    next_id += 1
    new_item = Item(id=next_id, name=item.name , description=item.description, price=item.price)
    items.append(new_item)
    return item


@app.get("/items/", response_model=list[Item])
def read_items():
    "Return the list of items"
    return items

