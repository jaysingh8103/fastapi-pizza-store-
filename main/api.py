"""FastAPI application and route handlers"""
from fastapi import FastAPI, Depends, HTTPException, status
from sqlitedict import SqliteDict
from typing import List

from main.models import Pizza, OrderItem, PriceUpdate
from main.database import get_db, get_menu, initialize_database
from main.config import DB_KEY

# Initialize database on import
initialize_database()

app = FastAPI(
    title="Pizza Store API",
    description="A REST API for managing a pizza store",
    version="1.0.0"
)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Pizza Store API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/pizza_names")
def pizza_names(db: SqliteDict = Depends(get_db)):
    """Get list of all pizza names"""
    menu = get_menu(db)
    names = [pizza["name"] for pizza in menu]
    return {"pizza_list": names}


@app.get("/pizza_details")
def detail_of_pizza(id: int, db: SqliteDict = Depends(get_db)):
    """Get details of a specific pizza by ID"""
    pizza_menu = get_menu(db)
    for pizza in pizza_menu:
        if pizza["id"] == id:
            return pizza
    return {"message": "id not found"}


@app.post("/order")
def place_order(order_items: List[OrderItem], db: SqliteDict = Depends(get_db)):
    """Place an order with multiple pizza items"""
    total_price = 0.0
    not_found_id = []
    pizza_menu = get_menu(db)
    found_any = False
    
    for item in order_items:
        pizza = next((p for p in pizza_menu if p["id"] == item.id), None)
        if pizza:
            total_price += pizza["price"] * item.quantity
            found_any = True
        else:
            not_found_id.append(item.id)
    
    if not found_any:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pizzas with IDs {not_found_id} not found."
        )
    
    return {
        "total_price": round(total_price, 2),
        "not_found_ids": not_found_id
    }


@app.put("/add_pizza")
def add_new_pizza(pizza: Pizza, db: SqliteDict = Depends(get_db)):
    """Add a new pizza to the menu"""
    pizza_menu = get_menu(db)
    
    if pizza_menu:
        new_id = max(p["id"] for p in pizza_menu) + 1
    else:
        new_id = 1
    
    pizza_data = pizza.model_dump()
    pizza_data["id"] = new_id
    pizza_menu.append(pizza_data)
    db[DB_KEY] = pizza_menu
    
    return {"message": "New pizza added successfully", "pizza_id": new_id}


@app.delete("/remove_pizza")
def remove_pizza(pizza_id: int, db: SqliteDict = Depends(get_db)):
    """Remove a pizza from the menu"""
    pizza_menu = get_menu(db)
    
    if pizza_menu:
        pizza_to_remove = next(
            (p for p in pizza_menu if p["id"] == pizza_id), 
            None
        )
    else:
        pizza_to_remove = None
    
    if not pizza_to_remove:
        return {"message": "Pizza ID not found"}
    
    pizza_menu.remove(pizza_to_remove)
    db[DB_KEY] = pizza_menu
    
    return {"message": "Pizza removed successfully"}


@app.patch("/update_price")
def update_pizza_price(data: PriceUpdate, db: SqliteDict = Depends(get_db)):
    """Update the price of a pizza"""
    pizza_menu = get_menu(db)
    
    if pizza_menu:
        pizza_to_update = next(
            (p for p in pizza_menu if p["id"] == data.pizza_id), 
            None
        )
    else:
        pizza_to_update = None
    
    if not pizza_to_update:
        return {"message": "Pizza ID not found"}
    
    pizza_to_update["price"] = data.new_price
    db[DB_KEY] = pizza_menu
    
    return {"message": "Pizza price updated successfully"}