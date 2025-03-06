from fastapi.testclient import TestClient
from oop import app, system, Menu

client = TestClient(app)

def test_add_menu():
    response = client.post("/add_menu/", json={
        "name": "Test Menu",
        "owner": "Test Owner",
        "menu_tag": "Test Tag",
        "how_to": "Test How To",
        "preparing_time": "10 mins",
        "making_itme": "5 mins",
        "size": "Medium",
        "calories": "200",
        "cost": "10"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Menu added successfully", "menu": {
        "name": "Test Menu",
        "owner": "Test Owner",
        "menu_tag": "Test Tag",
        "how_to": "Test How To",
        "preparing_time": "10 mins",
        "making_itme": "5 mins",
        "size": "Medium",
        "calories": "200",
        "cost": "10"
    }}

def test_get_all_menus():
    response = client.get("/menus")
    assert response.status_code == 200
    assert len(response.json()) > 0