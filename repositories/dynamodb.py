import boto3
from boto3.dynamodb.conditions import Key
from uuid import uuid4
from repositories.schemas import Workout, Set, Exercise
from datetime import date

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("fitness-app")

class DynamoWorkoutRepository:
    def _pk_user(self, user_id):
        return f"USER#{user_id}"

    def _pk_workout(self, workout_id):
        return f"WORKOUT#{workout_id}"

    def _pk_exercise(self, user_id, exercise_id):
        return f"USER#{user_id}", f"EXERCISE#{exercise_id}"

    # ------------------------
    # WORKOUTS
    # ------------------------
    def create_workout(self, user_id, data):
        workout_id = str(uuid4())

        table.put_item(Item={
            "PK": self._pk_workout(workout_id),
            "SK": "METADATA",
            "user_id": user_id,
            "workout_date": data.workout_date.isoformat()
        })

        return Workout(
            id=workout_id,
            workout_date=data.workout_date,
            sets=[]
        )

    def add_set(self, workout_id, data):
        set_id = str(uuid4())

        item = {
            "PK": self._pk_workout(workout_id),
            "SK": f"SET#{set_id}",
            **self._serialize_set(data)
        }

        table.put_item(Item=item)

        return self.get_workout(workout_id)

    def get_workout(self, workout_id):
        response = table.query(
            KeyConditionExpression=Key("PK").eq(self._pk_workout(workout_id))
        )

        items = response.get("Items", [])
        if not items:
            return None

        return self._deserialize_workout(items)

    def get_workouts_for_user(self, user_id):
        # Requires a GSI on user_id
        response = table.query(
            IndexName="user_id-index",
            KeyConditionExpression=Key("user_id").eq(user_id)
        )

        workouts = {}

        for item in response.get("Items", []):
            pk = item["PK"]
            workout_id = pk.split("#")[1]

            if workout_id not in workouts:
                workouts[workout_id] = []

            workouts[workout_id].append(item)

        return [
            self._deserialize_workout(items)
            for items in workouts.values()
        ]
    # ------------------------
    # EXERCISES
    # ------------------------

    def create_exercise(self, user_id, data):
        exercise_id = str(uuid4())
        pk, sk = self._pk_exercise(user_id, exercise_id)

        table.put_item(Item={
            "PK": pk,
            "SK": sk,
            "name": data.name,
            "movement_distance_m": data.movement_distance_m
        })

        return Exercise(
            id=exercise_id,
            name=data.name,
            movement_distance_m=data.movement_distance_m
        )

    def get_exercise(self, user_id, exercise_id):
        pk, sk = self._pk_exercise(user_id, exercise_id)

        response = table.get_item(Key={
            "PK": pk,
            "SK": sk
        })

        item = response.get("Item")
        if not item:
            return None

        return Exercise(
            id=exercise_id,
            name=item["name"],
            movement_distance_m=item["movement_distance_m"]
        )

    def list_exercises(self, user_id):
        response = table.query(
            KeyConditionExpression=Key("PK").eq(self._pk_user(user_id)) &
                                   Key("SK").begins_with("EXERCISE#")
        )

        exercises = []
        for item in response.get("Items", []):
            exercise_id = item["SK"].split("#")[1]

            exercises.append(Exercise(
                id=exercise_id,
                name=item["name"],
                movement_distance_m=item["movement_distance_m"]
            ))

        return exercises
    # ------------------------
    # SERIALIZATION
    # ------------------------

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
                    "id": item["PK"].split("#")[1],
                    "workout_date": date.fromisoformat(item["workout_date"])
                }
            else:
                sets.append({
                    "exercise_id": item["exercise_id"],
                    "exercise_name": item["exercise_name"],
                    "movement_distance_m": item["movement_distance_m"],
                    "weight_kg": item["weight_kg"],
                    "reps": item["reps"]
                })

        if workout is None:
            return None

        workout["sets"] = [Set(**s) for s in sets]
        return Workout(**workout)