import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:////tmp/fitness.db"

DB_BACKEND = os.getenv("DB_BACKEND", "sqlite")

if DB_BACKEND == "dynamodb":
    from db_dynamodb import create_workout, add_exercise, get_workout
else:
    from db_sqlite import create_workout, add_exercise, get_workout

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()