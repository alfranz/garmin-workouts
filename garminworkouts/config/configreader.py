import yaml
from garminworkouts.config.includeloader import IncludeLoader
from typing import Union
from garminworkouts.models.workout import Workout
from garminworkouts.models.running_workout import RunningWorkout
from pathlib import Path


def read_config(filename: Union[str, Path]) -> dict:
    with open(filename, "r") as f:
        data = yaml.load(f, IncludeLoader)
    return data


def parse_config(config: dict) -> Union[Workout, RunningWorkout]:
    if config["type"] == "running":
        return RunningWorkout(config)
    else:
        return Workout(config)
