from sqlalchemy.orm import Session
from repositories.db import SessionLocal
from repositories import models
from schemas import Workout, Set, Exercise
import uuid

class SQLiteWorkoutRepository:

    def _get_session(self) -> Session:
        return SessionLocal()

    def create_workout(self, user_id, data):
        return

    def add_set(self, workout_id, data):
        return

    def get_workout(self, workout_id):
        return

    def get_workouts_for_user(self, user_id):
        return

    def create_exercise(self, user_id, data):
        return

    def get_exercise(self, user_id, exercise_id):
        return

    def list_exercises(self, user_id):
        return
