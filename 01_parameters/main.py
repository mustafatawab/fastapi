from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id" : item_id }

@app.get("/items")
def limited_items(limit: int):
    return {"limit" : limit}