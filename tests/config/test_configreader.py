import os

from garminworkouts.config import configreader


def test_configreader():
    config_file = os.path.join(os.path.dirname(__file__), "test_configreader.yaml")
    config = configreader.read_config(config_file)

    expected_config = {
        "name": "Test",
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
