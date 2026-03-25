from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from repositories.models import Base, Workout, Set, Exercise
import uuid

engine = create_engine(
    "sqlite:///:memory:",  # in-memory for tests
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class SQLiteWorkoutRepository:
    def __init__(self, session=None):
        self.session = session or SessionLocal()

    # Add this class method:
    @classmethod
    def init_db(cls):
        Base.metadata.create_all(bind=engine)
    def _get_session(self) -> Session:
        return SessionLocal()

    def create_workout(self, user_id, data):
        db = self._get_session()
        try:
            workout = Workout(
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
            new_set = Set(
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
                Workout,
                Set,
                Exercise
            ).join(
                Set, Workout.id == Set.workout_id
            ).join(
                Exercise, Set.exercise_id == Exercise.id
            ).filter(
                Workout.id == int(workout_id)
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
            workouts = db.query(Workout).filter(
                Workout.user_id == user_id
            ).all()

            if not workouts:
                return None

            return [self.get_workout(str(w.id)) for w in workouts]
        finally:
            db.close()

    def create_exercise(self, user_id, data):
        db = self._get_session()
        try:
            exercise = Exercise(
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
            exercise = db.query(Exercise).filter(
                Exercise.id == int(exercise_id),
                Exercise.user_id == user_id
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
            exercises = db.query(Exercise).filter(
            Exercise.user_id == user_id).all()

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
