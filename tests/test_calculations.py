from services.calculations import (
    set_volume,
    set_work_joules,
    joules_to_calories
)


def test_set_volume():
    assert set_volume(100, 5) == 500


def test_set_work_joules():
    work = set_work_joules(weight_kg=100, reps=5, distance_m=0.5)
    assert work > 0


def test_joules_to_calories():
    calories = joules_to_calories(4184 * 0.25)
    assert round(calories, 2) == 1.0