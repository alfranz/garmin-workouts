import pytest
from garminworkouts.models.pace import Pace


@pytest.mark.parametrize(
    "pace_str, expected_minutes_per_km",
    [
        ("5:00", 5.0),
        ("5:15", 5.25),
        ("6:00", 6.0),
        ("6:30", 6.5),
    ],
)
def test_parse_pace(pace_str, expected_minutes_per_km):
    pace = Pace(pace_str)
    assert pace.minutes_per_km == expected_minutes_per_km


@pytest.mark.parametrize(
    "pace_str, expected_str",
    [
        ("5:00", "5:00"),
        ("5:30", "5:30"),
        ("6:45", "6:45"),
    ],
)
def test_str(pace_str, expected_str):
    pace = Pace(pace_str)
    assert str(pace) == expected_str


@pytest.mark.parametrize(
    "pace1_str, pace2_str, are_equal",
    [
        ("5:00", "5:00", True),
        ("5:00", "6:00", False),
    ],
)
def test_equality(pace1_str, pace2_str, are_equal):
    pace1 = Pace(pace1_str)
    pace2 = Pace(pace2_str)
    assert (pace1 == pace2) == are_equal


@pytest.mark.parametrize(
    "invalid_pace_str",
    ["invalid", "5:xx", "-5:00", "-5", "5:00:00", "5:00:00:00"],
)
def test_invalid_pace(invalid_pace_str):
    with pytest.raises(ValueError):
        Pace(invalid_pace_str)


if __name__ == "__main__":
    pytest.main()
