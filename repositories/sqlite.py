from sqlalchemy.orm import Session
from repositories.db import SessionLocal
from repositories import models
from schemas import Workout, Set, Exercise
import uuid

class SQLiteWorkoutRepository:

    def _get_session(self) -> Session:
        return SessionLocal()

    def create_workout(self, user_id, data):
        db = self._get_session()
        try:
            workout = models.Workout(
                user_id=user_id,
                date=data.workout_date
            )
            db.add(workout)
            db.commit()
            db.refresh(workout)

            return Workout(
                id=str(workout.id),
                workout_date=workout.date,
                sets=[]
            )
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def add_set(self, workout_id, data):
        db = self._get_session()
        try:
            new_set = models.Set(
                workout_id=int(workout_id),
                exercise_id=int(data.exercise_id),
                weight_kg=data.weight_kg,
                reps=data.reps
            )
            db.add(new_set)
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
        return self.get_workout(workout_id)

    def get_workout(self, workout_id):
        db = self._get_session()
        try:
            rows = db.query(
                models.Workout,
                models.Set,
                models.Exercise
            ).join(
                models.Set, models.Workout.id == models.Set.workout_id
            ).join(
                models.Exercise, models.Set.exercise_id == models.Exercise.id
            ).filter(
                models.Workout.id == int(workout_id)
            ).all()

            if not rows:
                return None

            workout = rows[0][0]

            sets = []
            for _, s, e in rows:
                sets.append(Set(
                    exercise_id=str(e.id),
                    exercise_name=e.name,
                    movement_distance_m=e.movement_distance_m,
                    weight_kg=s.weight_kg,
                    reps=s.reps
                ))

            return Workout(
                id=str(workout.id),
                workout_date=workout.date,
                sets=sets
            )
        finally:
            db.close()

    def get_workouts_for_user(self, user_id):
        db = self._get_session()
        try:
            workouts = db.query(models.Workout).filter(
                models.Workout.user_id == user_id
            ).all()

            if not workouts:
                return None

            return [self.get_workout(str(w.id)) for w in workouts]
        finally:
            db.close()

    def create_exercise(self, user_id, data):
        db = self._get_session()
        try:
            exercise = models.Exercise(
                name=data.name,
                movement_distance_m=data.movement_distance_m,
                user_id=user_id  # only if you added this column
            )
            db.add(exercise)
            db.commit()
            db.refresh(exercise)

            return Exercise(
                id=str(exercise.id),
                name=exercise.name,
                movement_distance_m=exercise.movement_distance_m
            )
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def get_exercise(self, user_id, exercise_id):
        db = self._get_session()
        try:
            exercise = db.query(models.Exercise).filter(
                models.Exercise.id == int(exercise_id),
                models.Exercise.user_id == user_id
            ).first()

            if not exercise:
                return None

            return Exercise(
                id=str(exercise.id),
                name=exercise.name,
                movement_distance_m=exercise.movement_distance_m
            )
        finally:
            db.close()

    def list_exercises(self, user_id):
        db = self._get_session()
        try:
            exercises = db.query(models.Exercise).filter(
            models.Exercise.user_id == user_id).all()

            if not exercises:
                return None
            return [
                Exercise(
                    id=str(e.id),
                    name=e.name,
                    movement_distance_m=e.movement_distance_m
                )
                for e in exercises
            ]
        finally:
            db.close()
