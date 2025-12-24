from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from collections import defaultdict
from mangum import Mangum

from db import SessionLocal, engine
from db import create_workout, add_exercise, get_workout
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

# Post an exercise
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

# Post a set
@app.post("/sets")
def add_set(
    set_data: SetCreate,
    db: Session = Depends(get_db)
):
    workout = db.query(Workout).filter(Workout.id == set_data.workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    exercise = db.query(Exercise).filter(Exercise.id == set_data.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

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

# Get a workout
@app.get("/workouts/{workout_id}/summary")
def workout_summary(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

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

# Get a history for a particular exercise
@app.get("/exercises/{exercise_id}/history")
def exercise_history(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # Fetch all sets for this exercise
    sets = (
        db.query(Set)
        .join(Workout)
        .filter(Set.exercise_id == exercise_id)
        .all()
    )

    # Group data by workout date
    history_by_date = defaultdict(lambda: {
        "total_sets": 0,
        "total_reps": 0,
        "total_volume_kg": 0.0,
        "total_work_joules": 0.0
    })

    for s in sets:
        workout_date = s.workout.date.isoformat()

        history_by_date[workout_date]["total_sets"] += 1
        history_by_date[workout_date]["total_reps"] += s.reps
        history_by_date[workout_date]["total_volume_kg"] += set_volume(
            s.weight_kg, s.reps
        )
        history_by_date[workout_date]["total_work_joules"] += set_work_joules(
            s.weight_kg,
            s.reps,
            exercise.movement_distance_m
        )

    # Format response
    history = []
    for date, data in sorted(history_by_date.items()):
        calories = joules_to_calories(data["total_work_joules"])
        history.append({
            "date": date,
            "total_sets": data["total_sets"],
            "total_reps": data["total_reps"],
            "total_volume_kg": round(data["total_volume_kg"], 2),
            "estimated_calories": round(calories, 2)
        })

    return {
        "exercise_id": exercise.id,
        "exercise_name": exercise.name,
        "history": history
    }

handler = Mangum(app)