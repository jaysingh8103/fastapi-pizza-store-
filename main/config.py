import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Database configuration - use environment variable or default
DB_PATH = Path(os.getenv("DB_PATH", BASE_DIR / "data" / "pizza_store.sqlite"))
DB_KEY = "pizza_menu"

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))