# Library Imports
from fastapi import FastAPI, HTTPException, Header, Depends
from mangum import Mangum

from repositories.schemas import WorkoutCreate, SetCreate, ExerciseCreate, Workout, Exercise, Set
from repositories.base import workout_repo
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

@app.post("/workouts", response_model=Workout)
def create_workout_endpoint(
    payload: WorkoutCreate,
    user_id: str = Depends(get_user_id)
):
    return create_workout(user_id, payload)


@app.post("/workouts/{workout_id}/sets", response_model=Set)
def add_set_endpoint(workout_id: str, payload: Set):
    # add the set to DB
    set_row = workout_repo.add_set(workout_id, payload)  # pass payload as a single argument
    # Return the created set (SQLAlchemy model)
    return Set.from_orm(set_row)


@app.get("/workouts/{workout_id}", response_model=Workout)
def get_workout_endpoint(workout_id: str):
    workout = get_workout(workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@app.get("/workouts", response_model=list[Workout])
def get_workouts_for_user_endpoint(
    user_id: str = Depends(get_user_id)
):
    return get_workouts_for_user(user_id)


# ------------------------
# EXERCISES
# ------------------------

@app.post("/exercises", response_model=Exercise)
def create_exercise_endpoint(
    payload: ExerciseCreate,
    user_id: str = Depends(get_user_id)
):
    return create_exercise(user_id, payload)


@app.get("/exercises", response_model=list[Exercise])
def list_exercises_endpoint(
    user_id: str = Depends(get_user_id)
):
    return list_exercises(user_id)


@app.get("/exercises/{exercise_id}", response_model=Exercise)
def get_exercise_endpoint(
    exercise_id: str,
    user_id: str = Depends(get_user_id)
):
    exercise = get_exercise(user_id, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


# ------------------------
# AWS Lambda handler
# ------------------------

handler = Mangum(app)
