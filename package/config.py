import os

DB_BACKEND = os.getenv("DB_BACKEND", "sqlite")

if DB_BACKEND not in {"sqlite", "dynamodb"}:
    raise ValueError(f"Invalid DB_BACKEND: {DB_BACKEND}")