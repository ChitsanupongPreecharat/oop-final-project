import testoop.oop as oop
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()
class Menuapi(BaseModel):
    name: str
    owner: str
    menu_tag: str
    how_to: str
    preparing_time: str
    making_itme: str
    size: str
    calories: str
    cost: str
    checked_by_admin: bool

system = oop.system

@app.get("/")
def read_root():
    return {"message": "Hello world! "}

@app.post("/add_menu")
def add_menu(menu: Menuapi = Body(...)):
    new_menu = system.add_menu(
        menu.name, menu.owner, menu.menu_tag, menu.how_to,
        menu.preparing_time, menu.making_itme, menu.size,
        menu.calories, menu.cost, menu.checked_by_admin
    )
    return {"message": "Added menu successfully", "menu_id": new_menu["menu_id"]}

@app.get("/menus")
def get_all_menus():
    return [menu.__dict__ for menu in system.get_all_menus()]

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}