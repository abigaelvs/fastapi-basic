from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


inventory = {
    1: {
        "name": "Milk",
        "price": 10000,
        "brand": "Regular"
    },
    2: {
        "name": "Eggs",
        "price": 10000,
        "brand": "Large"
    }
}


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


@app.get("/items/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item you'd like")):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist")
    return inventory[item_id]


@app.get("/items")
def get_items():
    return inventory


@app.get("/items/")
def get_by_name(name: str = Query(None, title="Name", description="The name of the item")):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    
    raise HTTPException(404, "Item not found")

        
@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item already exist")
    inventory[item_id] = item
    return inventory[item_id]


@app.put("/items/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist")

    if item.name != None:
        inventory[item_id]["name"] = item.name
    if item.price != None:
        inventory[item_id]["price"] = item.price
    if item.brand != None:
        inventory[item_id]["brand"] = item.brand

    return inventory[item_id]


@app.delete("/items")
def delete_item(item_id: int = Query(..., description="The ID of the item you want to delete")):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist")
    del inventory[item_id]
    raise HTTPException(status_code=200, detail="Item Deleted!")