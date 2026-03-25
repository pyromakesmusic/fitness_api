from config import DB_BACKEND
from repositories.sqlite import SQLiteWorkoutRepository
from repositories.dynamodb import DynamoWorkoutRepository
import os

DB_BACKEND = os.environ.get("DB_BACKEND", "sqlite").strip('"').lower()

if DB_BACKEND == "sqlite":
    from repositories.sqlite import SQLiteWorkoutRepository
    workout_repo = SQLiteWorkoutRepository()
    # initialize tables for SQLite
    SQLiteWorkoutRepository.init_db()
else:
    from repositories.dynamodb import DynamoWorkoutRepository
    workout_repo = DynamoWorkoutRepository()