from pydantic import BaseModel, Field
from datetime import date

class Exercise(BaseModel):
    id: str
    name: str
    movement_distance_m: float
class Set(BaseModel):
    exercise_id: str
    exercise_name: str
    movement_distance_m: float
    weight_kg: float
    reps: int

    class Config:
        from_attributes = True
        from_orm = True
class Workout(BaseModel):
    id: str
    workout_date: date
    sets: list[Set]

    class Config:
        from_attributes=True
        orm_mode = True
class ExerciseCreate(BaseModel):
    name: str = Field(..., min_length=1)
    movement_distance_m: float = Field(..., gt=0)

class SetCreate(BaseModel):
    exercise_id: str
    exercise_name: str
    movement_distance_m: float = Field(..., gt=0)
    weight_kg: float = Field(..., gt=0)
    reps: int = Field(..., gt=0)

class WorkoutCreate(BaseModel):
    user_id: str
    workout_date: date