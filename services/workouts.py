from repositories.base import workout_repo

def create_workout(data):
    return workout_repo.create_workout(data)

def add_exercise(workout_id, data):
    return workout_repo.add_exercise(workout_id, data)

def get_workout(workout_id):
    return workout_repo.get_workout(workout_id)

def exercise_history(user_id):
    workouts = workout_repo.get_workouts_for_user(user_id)
    # compute summaries here
    return workouts