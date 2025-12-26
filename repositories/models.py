from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)

    sets = relationship("Set", back_populates="workout")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    movement_distance_m = Column(Float, nullable=False)

    sets = relationship("Set", back_populates="exercise")


class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))

    weight_kg = Column(Float, nullable=False)
    reps = Column(Integer, nullable=False)

    workout = relationship("Workout", back_populates="sets")
    exercise = relationship("Exercise", back_populates="sets")