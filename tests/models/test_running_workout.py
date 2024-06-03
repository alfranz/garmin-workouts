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
            WorkoutStep(duration=600, zone="WU/CD"),
            WorkoutStep(distance=3000, zone="Easy"),
            WorkoutStep(duration=600, zone="WU/CD"),
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
    step = WorkoutStep(duration=600, zone="Easy")
    assert step.duration == 600
    assert step.zone == "Easy"
    assert step.distance is None


def test_init_workout_step_with_distance():
    step = WorkoutStep(distance=3000, zone="Easy")
    assert step.distance == 3000
    assert step.zone == "Easy"
    assert step.duration is None


def test_init_workout_step_with_both_distance_and_duration():
    with pytest.raises(ValueError):
        WorkoutStep(duration=600, distance=3000, zone="Easy")


def test_running_workout_repr(running_workout_config):
    workout = RunningWorkout(running_workout_config)
    assert repr(workout) == f"RunningWorkout({running_workout_config})"


def test_running_workout_summary_eq_str(running_workout_config):
    workout = RunningWorkout(running_workout_config)
    expected_summary = "Easy 5k Run: A very simple test running workout, 1km warmup, 3km easy pace, 1km cooldown"
    assert workout.get_workout_summary() == expected_summary
    assert str(workout) == workout.get_workout_summary()
