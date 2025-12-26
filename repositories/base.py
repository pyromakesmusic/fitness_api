from config import DB_BACKEND
from repositories.sqlite import SQLiteWorkoutRepository
from repositories.dynamodb import DynamoWorkoutRepository

if DB_BACKEND == "sqlite":
    workout_repo = SQLiteWorkoutRepository()
else:
    workout_repo = DynamoWorkoutRepository()