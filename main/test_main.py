import pytest
from fastapi.testclient import TestClient
from sqlitedict import SqliteDict
import os
from main import app, DB_PATH, DB_KEY


client = TestClient(app)
TEST_DB_PATH = "test_pizza_store.sqlite"
@pytest.fixture(autouse=True)
def setup_and_teardown():
    db = SqliteDict(TEST_DB_PATH, autocommit=True)
    sample_menu = [
        {
            "id": 1,
            "name": "Margherita",
            "size": "Medium",
            "price": 12.99,
            "toppings": ["tomato sauce", "mozzarella", "basil"]
        },
        {
            "id": 2,
            "name": "Pepperoni",
            "size": "Large",
            "price": 15.99,
            "toppings": ["tomato sauce", "mozzarella", "pepperoni"]
        },
        {
            "id": 3,
            "name": "Veggie Supreme",
            "size": "Medium",
            "price": 13.99,
            "toppings": ["tomato sauce", "mozzarella", "peppers", "onions", "mushrooms"]
        }
    ]
    db[DB_KEY] = sample_menu
    db.close()

    import main
    original_db_path = main.DB_PATH
    main.DB_PATH = TEST_DB_PATH
    
    yield

    main.DB_PATH = original_db_path
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


class TestPizzaNames:    
    def test_get_pizza_names_success(self):
        response = client.get("/pizza_names")
        assert response.status_code == 200
        data = response.json()
        assert "pizza_list" in data
        assert len(data["pizza_list"]) == 3
        assert "Margherita" in data["pizza_list"]
        assert "Pepperoni" in data["pizza_list"]
        assert "Veggie Supreme" in data["pizza_list"]
        
class TestPizzaDetails:
    def test_get_pizza_details_success(self):
        response = client.get("/pizza_details?id=1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Margherita"
        assert data["size"] == "Medium"
        assert data["price"] == 12.99
        assert "basil" in data["toppings"]
        
    def test_pizza_details_not_found(self):
        response = client.get("/pizza_details?id=999999")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "id not found"
        
class TestPizzaOrder:
    def test_place_for_one_iteam(self):
        order = [{"id":1 , "quantity":2}]
        response =client.post("/order", json=order)
        assert response.status_code == 200
        data = response.json()
        assert data["total_price"] == 25.98
        assert data["not_found_ids"] == []
        
    def test_place_for_multipul_iteams(self):
        order = [{"id":1, "quantity":2},{"id":2,"quantity":2}]
        response = client.post("/order", json=order)
        assert response.status_code == 200
        data = response.json()
        assert data["total_price"] == 57.96
        assert data["not_found_ids"] == []
        
    def test_place_for_not_found_iteams(self):
        order = [{"id":1, "quantity":2},{"id":2,"quantity":2},{"id":20220 , "quantity":12}]
        response = client.post("/order", json=order)
        assert response.status_code == 200
        data = response.json()
        assert data["total_price"] == 57.96
        assert 20220 in data ["not_found_ids"]  
        
    def test_both_id_are_not_found (self):
        order = [{"id":12, "quantity":2},{"id":33,"quantity":2}]
        response = client.post("/order", json=order)
        assert response.status_code == 404
        data = response.json()
        assert "not found" in response.json()["detail"]
        
    def test_both_are_empty(self):
        response = client.post("/order", json=[])
        assert response.status_code == 404
        
        
class TestPizzaAdd:
    def test_add_pizza(self):
        add = {
            "name": "Supreme",
            "size": "Medium",
            "price": 14.99,
            "toppings": ["tomato sauce", "mozzarella", "peppers", "onions", "mushrooms"]
        }
        
        response = client.put("/add_pizza",json=add)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "New pizza added successfully"
        assert data["pizza_id"] == 4
        
        verify_response = client.get("/pizza_details?id=4")
        assert verify_response.status_code == 200
        assert verify_response.json()["name"] == "Supreme"
        
        
    def test_find_negative_success(self):
        new_pizza = {
            "name": "Hawaiian",
            "size": "Large",
            "price": -14.99,
            "toppings": ["tomato sauce", "mozzarella", "ham", "pineapple"]
        }
        response = client.put("/add_pizza", json=new_pizza)
        assert response.status_code == 422
       
class TestRemove:
    def test_to_remove(self):
        response = client.delete("/remove_pizza?pizza_id=2")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Pizza removed successfully"
        
        verify_response = client.get("/pizza_details?id=2")
        assert verify_response.json()["message"] == "id not found"  
        
    def test_remove_pizza_not_found(self):
        response = client.delete("/remove_pizza?pizza_id=999")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Pizza ID not found"
    
    
    
    
    
        
                
        
        
        
        


