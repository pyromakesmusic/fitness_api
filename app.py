# Library Imports
from fastapi import FastAPI, HTTPException, Header
from mangum import Mangum

from repositories.schemas import WorkoutCreate, SetCreate, ExerciseCreate
from services.workouts import (
    create_workout,
    add_set,
    get_workout,
    get_workouts_for_user,
    create_exercise,
    get_exercise,
    list_exercises,
)

app = FastAPI(title="Fitness Tracking API")


# ------------------------
# Helper: user_id extraction
# ------------------------

def get_user_id(x_user_id: str = Header(...)):
    return x_user_id


# ------------------------
# WORKOUTS
# ------------------------

@app.post("/workouts")
def create_workout_endpoint(
    payload: WorkoutCreate,
    user_id: str = Header(..., alias="X-User-Id")
):
    return create_workout(user_id, payload)


@app.post("/workouts/{workout_id}/sets")
def add_set_endpoint(
    workout_id: str,
    payload: SetCreate
):
    return add_set(workout_id, payload)


@app.get("/workouts/{workout_id}")
def get_workout_endpoint(workout_id: str):
    workout = get_workout(workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@app.get("/workouts")
def get_workouts_for_user_endpoint(
    user_id: str = Header(..., alias="X-User-Id")
):
    return get_workouts_for_user(user_id)


# ------------------------
# EXERCISES
# ------------------------

@app.post("/exercises")
def create_exercise_endpoint(
    payload: ExerciseCreate,
    user_id: str = Header(..., alias="X-User-Id")
):
    return create_exercise(user_id, payload)


@app.get("/exercises")
def list_exercises_endpoint(
    user_id: str = Header(..., alias="X-User-Id")
):
    return list_exercises(user_id)


@app.get("/exercises/{exercise_id}")
def get_exercise_endpoint(
    exercise_id: str,
    user_id: str = Header(..., alias="X-User-Id")
):
    exercise = get_exercise(user_id, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


# ------------------------
# AWS Lambda handler
# ------------------------

handler = Mangum(app)