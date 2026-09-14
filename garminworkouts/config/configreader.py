from pathlib import Path

import yaml

from garminworkouts.config.includeloader import IncludeLoader
from garminworkouts.models.distance import Distance
from garminworkouts.models.duration import Duration
from garminworkouts.models.pace import PaceRange
from garminworkouts.models.running_workout import (
    RunningWorkout,
    RunningWorkoutConfig,
    WorkoutStep,
)
from garminworkouts.models.workout import Workout


def read_config(filename: str | Path) -> dict:
    with open(filename, "r") as f:
        data = yaml.load(f, IncludeLoader)
    return data


def parse_config(config: dict) -> Workout | RunningWorkout:
    if config["settings"]["sports_type"] == "running":
        zones = [
            PaceRange.from_str(z_name, zone_str)
            for z_name, zone_str in config["settings"]["zones"].items()
        ]
        workout_steps = []
        for step in config["steps"]:
            duration = step.get("duration")
            if duration:
                duration = Duration(duration).to_seconds()
            distance = step.get("distance")
            if distance:
                distance = Distance(distance).distance_meters

            workout_steps.append(
                WorkoutStep(
                    duration=duration,
                    distance=distance,
                    zone=step["zone"],
                )
            )

        run_config = RunningWorkoutConfig(
            name=config["name"],
            description=config.get("description", ""),
            zones=zones,
            steps=workout_steps,
        )
        return RunningWorkout(run_config)
    else:
        return Workout(config)


def read_workout(file: str) -> RunningWorkout:
    config = read_config(file)
    return parse_config(config)
