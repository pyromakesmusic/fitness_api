from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date

from db import SessionLocal, engine
from models import Base, Workout, Exercise, Set
from calculations import set_volume, set_work_joules, joules_to_calories
from schemas import ExerciseCreate, WorkoutCreate, SetCreate

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
    exercise: ExerciseCreate,
    db: Session = Depends(get_db)
):
    new_exercise = Exercise(
        name=exercise.name,
        movement_distance_m=exercise.movement_distance_m
    )
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    return new_exercise

@app.post("/workouts")
def create_workout(
    workout: WorkoutCreate,
    db: Session = Depends(get_db)
):
    new_workout = Workout(date=workout.workout_date)
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return new_workout

@app.post("/sets")
def add_set(
    set_data: SetCreate,
    db: Session = Depends(get_db)
):
    new_set = Set(
        workout_id=set_data.workout_id,
        exercise_id=set_data.exercise_id,
        weight_kg=set_data.weight_kg,
        reps=set_data.reps
    )
    db.add(new_set)
    db.commit()
    db.refresh(new_set)
    return new_set

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