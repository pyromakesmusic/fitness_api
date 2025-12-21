from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date

from db import SessionLocal, engine
from models import Base, Workout, Exercise, Set
from calculations import set_volume, set_work_joules, joules_to_calories

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Tracking API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/exercises")
def create_exercise(
    name: str,
    movement_distance_m: float,
    db: Session = Depends(get_db)
):
    exercise = Exercise(
        name=name,
        movement_distance_m=movement_distance_m
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise

@app.post("/workouts")
def create_workout(
    workout_date: date,
    db: Session = Depends(get_db)
):
    workout = Workout(date=workout_date)
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout

@app.post("/sets")
def add_set(
    workout_id: int,
    exercise_id: int,
    weight_kg: float,
    reps: int,
    db: Session = Depends(get_db)
):
    s = Set(
        workout_id=workout_id,
        exercise_id=exercise_id,
        weight_kg=weight_kg,
        reps=reps
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@app.get("/workouts/{workout_id}/summary")
def workout_summary(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()

    total_sets = len(workout.sets)
    total_reps = sum(s.reps for s in workout.sets)
    total_volume = sum(set_volume(s.weight_kg, s.reps) for s in workout.sets)

    total_work_joules = sum(
        set_work_joules(
            s.weight_kg,
            s.reps,
            s.exercise.movement_distance_m
        )
        for s in workout.sets
    )

    calories = joules_to_calories(total_work_joules)

    return {
        "total_sets": total_sets,
        "total_reps": total_reps,
        "total_volume_kg": round(total_volume, 2),
        "estimated_calories": round(calories, 2)
    }