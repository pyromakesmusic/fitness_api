from pydantic import BaseModel, Field
from datetime import date


class ExerciseCreate(BaseModel):
    name: str = Field(..., min_length=1)
    movement_distance_m: float = Field(..., gt=0)


class WorkoutCreate(BaseModel):
    workout_date: date


class SetCreate(BaseModel):
    workout_id: int
    exercise_id: int
    weight_kg: float = Field(..., gt=0)
    reps: int = Field(..., gt=0)