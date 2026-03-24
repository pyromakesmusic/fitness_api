from config import DB_BACKEND
from repositories.sqlite import SQLiteWorkoutRepository
from repositories.dynamodb import DynamoWorkoutRepository
import os

# Decide backend (default to sqlite if not set)
DB_BACKEND = os.environ.get("DB_BACKEND", "sqlite")  # <-- use environment variable

if DB_BACKEND == "sqlite":
    from repositories.sqlite import SQLiteWorkoutRepository
    workout_repo = SQLiteWorkoutRepository()
else:
    from repositories.dynamodb import DynamoWorkoutRepository
    workout_repo = DynamoWorkoutRepository()