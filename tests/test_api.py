from fastapi.testclient import TestClient
from app import app
import os

# Force SQLite for tests
os.environ["DB_BACKEND"] = "sqlite"

client = TestClient(app)

TEST_USER_ID = "test-user"


def headers():
    return {"X-User-Id": TEST_USER_ID}


# ------------------------
# Happy path test
# ------------------------

def test_full_workout_flow():
    # Create exercise
    response = client.post(
        "/exercises",
        headers=headers(),
        json={
            "name": "Test Squat",
            "movement_distance_m": 0.5
        }
    )
    assert response.status_code == 200
    exercise_id = response.json()["id"]

    # Create workout
    response = client.post(
        "/workouts",
        headers=headers(),
        json={"workout_date": "2025-01-01"}
    )
    assert response.status_code == 200
    workout_id = response.json()["id"]

    # Add set
    response = client.post(
        f"/workouts/{workout_id}/sets",
        headers=headers(),
        json={
            "exercise_id": exercise_id,
            "exercise_name": "Test Squat",
            "movement_distance_m": 0.5,
            "weight_kg": 100,
            "reps": 5
        }
    )
    assert response.status_code == 200

    # Get workout
    response = client.get(f"/workouts/{workout_id}", headers=headers())
    assert response.status_code == 200

    workout = response.json()
    assert len(workout["sets"]) == 1
    s = workout["sets"][0]
    assert s["reps"] == 5
    assert s["weight_kg"] == 100


# ------------------------
# Error handling test
# ------------------------

def test_workout_not_found():
    response = client.get("/workouts/nonexistent-workout", headers=headers())
    assert response.status_code == 404
    assert response.json()["detail"] == "Workout not found"