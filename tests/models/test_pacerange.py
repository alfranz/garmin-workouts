import pytest
from garminworkouts.models.pace import PaceRange
from garminworkouts.models.pace import Pace


@pytest.mark.parametrize(
    "name, lower, upper, pace_str, expected_result",
    [
        ("MP (Marathon Pace)", Pace("4:30"), Pace("4:40"), "4:35", True),
        ("MP (Marathon Pace)", Pace("4:30"), Pace("4:40"), "4:45", False),
        ("Tempo", Pace("3:50"), Pace("4:00"), "3:55", True),
        ("Tempo", Pace("3:50"), Pace("4:00"), "4:10", False),
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
            "MP (Marathon Pace)",
            Pace("4:30"),
            Pace("4:40"),
            "MP (Marathon Pace): 4:30 - 4:40",
        ),
        ("Tempo", Pace("3:50"), Pace("4:00"), "Tempo: 3:50 - 4:00"),
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
        PaceRange("Invalid Range", Pace(lower), Pace(upper))
