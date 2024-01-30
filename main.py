from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name : str
    price : float
    brand : Optional[str] = None
    
class UpdateItem(BaseModel):
    name : Optional[str] = None
    price : Optional[float] = None
    brand : Optional[str] = None
    

inventory = {}
#To retrieve the data from database
@app.get("/get_price/{item_name}")
def get_price(item_name:str, quantity: int): #item_id -> variable path component; item_name, quantity -> query parameters
    # raise ValueError(inventory)
    for id,v in inventory.items():
        if item_name in v.name:
            item_price = v.price
            total_price = item_price * quantity
            return {"item_name": item_name, "quantity": quantity, "total_cost": total_price}
        
    return {"error": "items not found"}

#endpoint url would look like http://your-server-address/get_price/15?item_name=t-shirt&quantity=2

#To create new data into the database
@app.post("/create_item/{item_id}")
def create_item(item_id: int, item: Item):
    # raise ValueError(item)
    if item_id in inventory:
        return {item_id : "already exists"}
    inventory[item_id] = dict(item)
    
    return inventory 
  

#To update the data that is already present in database
@app.put("/update_item/{item_id}")
def update_item(item_id:int, update_item: UpdateItem):
    if item_id not in inventory:
        return {item_id : "doesn't exist"}
    if update_item.name is not None: 
        inventory[item_id]["name"] = update_item.name
    if update_item.price is not None: 
        inventory[item_id]["price"] = update_item.price
    if update_item.brand is not None: 
        inventory[item_id]["brand"] = update_item.brand
    
    return inventory[item_id]
        
@app.delete("/delete_item/{item_id}")
def delete_item(item_id: int):
    if item_id in inventory:
        del inventory[item_id]
        return inventory
    return {item_id:" item not exists"}
    

#path parameter are basically a source mentioned in the URL following "/"
#query parameters are retrieved from the specific source mentioned after "?"
#like in update_item(), source is item_id and updated_item is choosing which category
#https:<server_address>/update_item/<path_parameter ex: item_id>?<updated_item>&<another query parameter>

