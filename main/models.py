"""Pydantic models for request/response validation"""
from pydantic import BaseModel, Field
from typing import List


class Pizza(BaseModel):
    """Pizza model for creating new pizzas"""
    name: str
    size: str
    price: float = Field(gt=0, description="Price must be greater than zero")
    toppings: List[str]


class OrderItem(BaseModel):
    """Order item model for placing orders"""
    id: int
    quantity: int


class PriceUpdate(BaseModel):
    """Model for updating pizza prices"""
    pizza_id: int
    new_price: float = Field(gt=0, description="Price must be greater than zero")