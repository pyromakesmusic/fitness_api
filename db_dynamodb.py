import os
import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def create_workout(user_id: str):
    workout_id = datetime.utcnow().isoformat()

    item = {
        "PK": f"USER#{user_id}",
        "SK": f"WORKOUT#{workout_id}",
        "type": "workout",
        "date": workout_id,
        "total_volume": 0,
    }

    table.put_item(Item=item)
    return workout_id


def add_exercise(user_id, workout_id, exercise):
    item = {
        "PK": f"USER#{user_id}",
        "SK": f"WORKOUT#{workout_id}#EXERCISE#{exercise.name}",
        "type": "exercise",
        "name": exercise.name,
        "sets": exercise.sets,
        "reps": exercise.reps,
        "weight": exercise.weight,
        "distance_m": exercise.distance_m,
        "volume": exercise.volume,
    }

    table.put_item(Item=item)


def get_workout(user_id, workout_id):
    response = table.query(
        KeyConditionExpression=
        "PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"USER#{user_id}",
            ":sk": f"WORKOUT#{workout_id}",
        }
    )
    return response["Items"]