GRAVITY = 9.81
HUMAN_EFFICIENCY = 0.25
JOULES_PER_CALORIE = 4184


def set_volume(weight_kg: float, reps: int) -> float:
    return weight_kg * reps


def set_work_joules(weight_kg: float, reps: int, distance_m: float) -> float:
    return weight_kg * GRAVITY * distance_m * reps


def joules_to_calories(joules: float) -> float:
    return joules / (JOULES_PER_CALORIE * HUMAN_EFFICIENCY)