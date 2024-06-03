import os
import pytest
from garminworkouts.config.configreader import read_config, parse_config


def get_test_file(filename: str):
    config_file = os.path.join(os.path.dirname(__file__), "workouts", filename)
    return config_file


def test_configreader_cycling():
    config_file = get_test_file("cycling/test_configreader.yaml")
    config = read_config(config_file)

    expected_config = {
        "name": "Cycling Test",
        "settings": {
            "sports_type": "cycling",
            "ftp": 250,
        },
        "steps": [
            [{"power": 50, "duration": "2:00"}],
            [{"power": 90, "duration": "12:00"}, {"power": 60, "duration": "4:00"}],
            [{"power": 90, "duration": "12:00"}, {"power": 60, "duration": "4:00"}],
            [{"power": 50, "duration": "2:00"}],
        ],
    }
    assert config == expected_config


def test_configreader_running():
    config_file = get_test_file("running/test_configreader.yaml")
    config = read_config(config_file)

    expected_config = {
        "name": "Running 30 Min",
        "description": "5 min easy, 20 min tempo, 1km rest",
        "settings": {
            "sports_type": "running",
            "zones": {"easy": "5:00-5:25", "tempo": "4:10-4:20", "rest": "5:30-10:00"},
        },
        "steps": [
            {"zone": "easy", "duration": "5:00"},
            {"zone": "tempo", "duration": "20:00"},
            {"zone": "rest", "distance": "1km"},
        ],
    }
    assert config == expected_config


def test_parse_config_running():
    config_file = get_test_file("running/test_configreader.yaml")
    config = read_config(config_file)
    workout = parse_config(config)
    assert workout.__class__.__name__ == "RunningWorkout"


@pytest.mark.skip("Skip until repeat intervals have been implemented.")
def test_parse_config_running_10k():
    config_file = get_test_file("running/test_10k.yaml")
    config = read_config(config_file)
    print(config)

    workout = parse_config(config)
    assert workout.get_workout_name == "Easy 10K with some strides"
