from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app import app, get_db
from models import Base

# Create in-memory test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Happy path test
def test_full_workout_flow():
    # Create exercise
    response = client.post("/exercises", json={
        "name": "Test Squat",
        "movement_distance_m": 0.5
    })
    assert response.status_code == 200
    exercise_id = response.json()["id"]

    # Create workout
    response = client.post("/workouts", json={
        "workout_date": "2025-01-01"
    })
    assert response.status_code == 200
    workout_id = response.json()["id"]

    # Add set
    response = client.post("/sets", json={
        "workout_id": workout_id,
        "exercise_id": exercise_id,
        "weight_kg": 100,
        "reps": 5
    })
    assert response.status_code == 200

    # Get summary
    response = client.get(f"/workouts/{workout_id}/summary")
    assert response.status_code == 200

    data = response.json()
    assert data["total_sets"] == 1
    assert data["total_reps"] == 5
    assert data["total_volume_kg"] == 500

# Error handling test

def test_workout_not_found():
    response = client.get("/workouts/999/summary")
    assert response.status_code == 404
    assert response.json()["detail"] == "Workout not found"

