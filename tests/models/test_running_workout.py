import pytest

from garminworkouts.models.running_workout import (
    RunningWorkout,
    RunningWorkoutConfig,
    WorkoutStep,
)

from garminworkouts.models.pace import PaceRange


@pytest.fixture
def running_workout_config():
    sample_config = RunningWorkoutConfig(
        name="Easy 5k Run",
        description="A very simple test running workout, 1km warmup, 3km easy pace, 1km cooldown",
        zones=[PaceRange("WU/CD", "5:20", "6:00"), PaceRange("Easy", "5:30", "6:00")],
        steps=[
            WorkoutStep(duration=600, target="WU/CD"),
            WorkoutStep(distance=3000, target="Easy"),
            WorkoutStep(duration=600, target="WU/CD"),
        ],
    )
    return sample_config


def test_running_workout_creation(running_workout_config):
    workout = RunningWorkout(running_workout_config)
    assert workout.config == running_workout_config
    workout_data = workout.create_workout()
    assert workout_data["workoutName"] == running_workout_config.name
    assert workout_data["description"] == running_workout_config.description


def test_init_workout_step():
    step = WorkoutStep(duration=600, target="Easy")
    assert step.duration == 600
    assert step.target == "Easy"
    assert step.distance is None


def test_init_workout_step_with_distance():
    step = WorkoutStep(distance=3000, target="Easy")
    assert step.distance == 3000
    assert step.target == "Easy"
    assert step.duration is None


def test_init_workout_step_with_both_distance_and_duration():
    with pytest.raises(ValueError):
        WorkoutStep(duration=600, distance=3000, target="Easy")
