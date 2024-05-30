import pytest
from garminworkouts.models.pace import PaceRange
from garminworkouts.models.pace import Pace


@pytest.mark.parametrize(
    "name, lower, upper, pace_str, expected_result",
    [
        ("MP", "4:30", "4:40", "4:35", True),
        ("MP", "4:30", "4:40", "4:45", False),
        ("Tempo", "3:50", "4:00", "3:55", True),
        ("Tempo", "3:50", "4:00", "4:10", False),
    ],
)
def test_pace_range_contains(name, lower, upper, pace_str, expected_result):
    pace_range = PaceRange(name, lower, upper)
    pace = Pace(pace_str)
    assert pace_range.contains(pace) == expected_result


@pytest.mark.parametrize(
    "name, lower, upper, expected_str",
    [
        (
            "MP",
            "4:30",
            "4:40",
            "MP: 4:30 - 4:40",
        ),
        ("Tempo", "3:50", "4:00", "Tempo: 3:50 - 4:00"),
    ],
)
def test_pace_range_str(name, lower, upper, expected_str):
    pace_range = PaceRange(name, lower, upper)
    assert str(pace_range) == expected_str


@pytest.mark.parametrize(
    "lower, upper",
    [
        ("5:00", "invalid"),
        ("invalid", "5:00"),
        ("5:00", "5:00:00"),
        ("5:00", "4:00"),
    ],
)
def test_invalid_pace_range(lower, upper):
    with pytest.raises(ValueError):
        PaceRange("Invalid Range", lower, upper)


def test_pace_range_bounds():
    lower = "4:30"
    upper = "4:40"
    pace_range = PaceRange("MP", lower, upper)
    assert pace_range.bounds == (Pace(lower), Pace(upper))


def test_pace_range_repr():
    lower = "4:30"
    upper = "4:40"
    pace_range = PaceRange("MP", lower, upper)
    assert repr(pace_range) == f"PaceRange('MP', {Pace(lower)}, {Pace(upper)})"


def test_parse_pace_range():
    pace_range = PaceRange.from_str("MP", "4:30 - 4:40")
    assert pace_range.name == "MP"
    assert pace_range.low == Pace("4:30")
    assert pace_range.high == Pace("4:40")
