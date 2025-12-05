# 🍕 Pizza Store API (FastApi and SQLITEDIST )

A small, production-ready REST API for managing a pizza store built with FastAPI, Pydantic and SqliteDict. Containerized with Docker + Docker Compose for easy deployment.

Quick highlights:
- Menu management: list, view details, add, remove, update price
- Orders: place multi-item orders with quantity and automatic price calculation
- Storage: persistent SQLite-backed dictionary via SqliteDict (supports Docker volumes)
- Pre-loaded with 10 common pizzas for convenience

---

## Table of contents
- [Quick start](#quick-start)
- [Run locally](#run-locally)
- [API endpoints](#api-endpoints)
- [Database](#database)
- [Docker](#docker)
- [Configuration](#configuration)
- [Project layout](#project-layout)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Quick start

1. Clone or open the project directory in VS Code (Windows example path shown above).
2. Create and activate a virtual environment:
   - Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - macOS / Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install dependencies:
   ```
   pip install -e .
   # or
   pip install -r requirements.txt
   ```
4. Initialize the database (creates file and pre-loads default pizzas):
   ```
   python -c "from main.database import initialize_database; initialize_database()"
   ```
5. Run the app:
   ```
   uvicorn main.api:app --reload
   ```
   Open http://localhost:8000/docs for interactive API docs (Swagger UI).

---

## Run locally (custom port / host)

Example using a custom port:
```
uvicorn main.api:app --host 0.0.0.0 --port 8080 --reload
```

---

## API endpoints (summary)

Base URL: http://localhost:8000

- GET `/`  
  Welcome message and API information.

- GET `/pizza_names`  
  Returns: `{ "pizza_list": ["Margherita", "Pepperoni", ...] }`

- GET `/pizza_details?id={id}`  
  Query parameter: `id` (int)  
  Returns pizza object: `{ "id": 1, "name": "Margherita", "size": "Medium", "price": 8.99, "toppings": [...] }`

- POST `/order`  
  Request body: list of items:
  ```
  [
    { "id": 1, "quantity": 2 },
    { "id": 3, "quantity": 1 }
  ]
  ```
  Response:
  ```
  {
    "total_price": 28.97,
    "not_found_ids": []
  }
  ```

- PUT `/add_pizza`  
  Add a new pizza:
  ```
  {
    "name": "Supreme",
    "size": "Large",
    "price": 14.99,
    "toppings": ["pepperoni", "sausage", "peppers", "onions"]
  }
  ```
  Response: `{ "message": "New pizza added successfully", "pizza_id": 11 }`

- DELETE `/remove_pizza?pizza_id={id}`  
  Remove pizza by id. Response: `{ "message": "Pizza removed successfully" }`

- PATCH `/update_price`  
  Update pizza price:
  ```
  {
    "pizza_id": 1,
    "new_price": 9.99
  }
  ```
  Response: `{ "message": "Pizza price updated successfully" }`

Use the interactive docs at `/docs` to view request/response schemas.

---

## Database

- Uses SqliteDict (SQLite-backed persistent dict).
- Default DB path: `data/pizza_store.sqlite` (configurable via env var).
- The repo initializes the database and preloads 10 popular pizzas.

Pre-loaded pizzas (names & example prices):
1. Margherita — $8.99
2. Pepperoni — $9.99
3. Vegetarian — $10.99
4. Hawaiian — $11.99
5. BBQ Chicken — $12.99
6. Cheese — $9.99
7. Mushroom — $10.99
8. Spinach and Feta — $11.99
9. Meat Lover's — $12.99
10. Buffalo Chicken — $13.99

---

## Docker

Recommended: Docker Compose.

- Build and start:
  ```
  docker-compose up -d --build
  ```
- View logs:
  ```
  docker-compose logs -f
  ```
- Stop:
  ```
  docker-compose down
  ```
- Stop and remove volumes (DELETES database):
  ```
  docker-compose down -v
  ```

Direct Docker usage:
```
docker build -f Dockerfile -t pizzaa-app .
docker run -d --name pizzaa-app -p 8000:8000 -v pizzaa-db:/app/data -e DB_PATH=/app/data/pizza_store.sqlite pizzaa-app
```

The DB is stored in the Docker volume `pizzaa-db` mounted at `/app/data` to persist data.

---

## Configuration (env vars)

- DB_PATH — path to SQLite DB file (default: `data/pizza_store.sqlite`)
- API_HOST — host to bind (default: `0.0.0.0`)
- API_PORT — port to bind (default: `8000`)

Set env vars in your shell, or in Docker Compose file for containerized runs.

---

## Project layout

- `main/api.py` — FastAPI application and route handlers  
- `main/models.py` — Pydantic models for requests & responses  
- `main/database.py` — DB helpers and initialization logic  
- `main/config.py` — configuration and environment handling  
- `Dockerfile`, `docker-compose.yml` — containerization

---

## Troubleshooting

- Database not created:
  - Ensure `data` directory exists and is writable.
  - Run the initialize command shown above.
- Port already in use:
  - Change port in `docker-compose.yml` or run uvicorn on another port.
- Import errors:
  - Activate virtualenv and install requirements:
    ```
    pip install -e .
    ```

---

## Testing (examples)

Get pizza names:
```
curl http://localhost:8000/pizza_names
```

Get pizza details:
```
curl "http://localhost:8000/pizza_details?id=1"
```

Place an order:
```
curl -X POST http://localhost:8000/order \
  -H "Content-Type: application/json" \
  -d '[{"id":1,"quantity":2},{"id":2,"quantity":1}]'
```

Add a pizza:
```
curl -X PUT http://localhost:8000/add_pizza \
  -H "Content-Type: application/json" \
  -d '{"name":"Supreme","size":"Large","price":14.99,"toppings":["pepperoni","sausage"]}'
```

---

## License
Open source — educational purposes.

---