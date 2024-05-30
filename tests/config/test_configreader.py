import os

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
        "description": "5 min easy, 20 min tempo, 5 min rest",
        "settings": {
            "sports_type": "running",
            "zones": {"easy": "5:00-5:25", "tempo": "4:10-4:20", "rest": "5:30-10:00"},
        },
        "steps": [
            {"target": "easy", "duration": "5:00"},
            {"target": "tempo", "duration": "20:00"},
            {"target": "rest", "duration": "5:00"},
        ],
    }
    assert config == expected_config


def test_parse_config_running():
    config_file = get_test_file("running/test_configreader.yaml")
    config = read_config(config_file)
    workout = parse_config(config)
    assert workout.__class__.__name__ == "RunningWorkout"
