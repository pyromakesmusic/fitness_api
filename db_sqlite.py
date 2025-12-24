# Library imports
from fastapi import FastAPI, Depends, HTTPException
from db import SessionLocal, engine
from sqlalchemy.orm import Session


from models import Base, Workout, Exercise, Set
from schemas import ExerciseCreate, WorkoutCreate, SetCreate


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Post a workout
# @app.post("/workouts")
def create_workout(
    workout: WorkoutCreate,
    db: Session = Depends(get_db)
):
    new_workout = Workout(date=workout.workout_date)
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return new_workout
