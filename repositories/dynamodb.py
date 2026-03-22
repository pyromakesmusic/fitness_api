class DynamoWorkoutRepository:
    def _pk_user(self, user_id):
        return f"USER#{user_id}"

    def create_workout(self, user_id, data):
        return

    def add_set(self, workout_id, data):
        return self.get_workout(workout_id)

    def get_workout(self, workout_id):
        return

    def _pk_workout(self, workout_id):
        return f"WORKOUT#{workout_id}"

    def get_workouts_for_user(self, user_id):
        return

    def create_exercise(self, user_id, data):
        return
    def _pk_exercise(self, user_id, exercise_id):
        return f"USER#{user_id}", f"EXERCISE#{exercise_id}"

    def get_exercise(self, user_id, exercise_id):
        return

    def list_exercises(self, user_id):
        return

    def _serialize_set(self, data):
        return {
        "exercise_id": data.exercise_id,
        "exercise_name": data.exercise_name,
        "movement_distance_m": data.movement_distance_m,
        "weight_kg": data.weight_kg,
        "reps": data.reps,
    }

    def _deserialize_workout(self, items):
        workout = None
        sets = []

        for item in items:
            if item["SK"] == "METADATA":
                workout = {
                    "id": ...,
                    "workout_date": ...
                }
            else:
                sets.append({
                    "exercise_id": ...,
                    "exercise_name": ...,
                    "movement_distance_m": ...,
                    "weight_kg": ...,
                    "reps": ...
                })

        workout["sets"] = sets
        return workout