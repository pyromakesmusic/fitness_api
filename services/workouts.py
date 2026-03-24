from repositories.base import workout_repo

def create_exercise(user_id, data):
    return workout_repo.create_exercise(user_id, data)

def get_exercise(user_id, exercise_id):
    return workout_repo.get_exercise(user_id, exercise_id)

def list_exercises(user_id):
    return workout_repo.list_exercises(user_id)
def create_workout(user_id, data):
    return workout_repo.create_workout(user_id, data)

def add_set(workout_id, data):
    return workout_repo.add_set(workout_id, data)

def get_workout(workout_id):
    return workout_repo.get_workout(workout_id)

def get_workouts_for_user(user_id):
    workouts = workout_repo.get_workouts_for_user(user_id)

    # compute summaries here if needed
    return workouts