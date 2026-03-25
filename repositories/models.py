from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from uuid import uuid4

Base = declarative_base()


class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    movement_distance_m = Column(Float, nullable=False)

class Workout(Base):
    __tablename__ = "workouts"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    workout_date = Column(Date, nullable=False)
    sets = relationship("Set", back_populates="workout")

class Set(Base):
    __tablename__ = "sets"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    workout_id = Column(String, ForeignKey("workouts.id"))
    exercise_id = Column(String, ForeignKey("exercises.id"))
    weight_kg = Column(Float, nullable=False)
    reps = Column(Integer, nullable=False)
    workout = relationship("Workout", back_populates="sets")