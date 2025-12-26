# Library Imports

from fastapi import FastAPI, Depends, HTTPException
from mangum import Mangum

from services.workouts import (
    create_workout,
    add_exercise,
    get_workout,
    exercise_history,
)


app = FastAPI(title="Fitness Tracking API")

@app.post("/workouts")
def create_workout_endpoint(payload: dict):
    return create_workout(payload)

@app.post("/workouts/{workout_id}/exercises")
def add_exercise_endpoint(workout_id: str, payload: dict):
    return add_exercise(workout_id, payload)

@app.get("/workouts/{workout_id}")
def get_workout_endpoint(workout_id: str):
    return get_workout(workout_id)

handler = Mangum(app)