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


def test_greater_than():
    pace1 = Pace("5:00")
    pace2 = Pace("6:00")
    assert pace2 > pace1


def test_less_than():
    pace1 = Pace("5:00")
    pace2 = Pace("6:00")
    assert pace1 < pace2


def test_greater_than_or_equal():
    pace1 = Pace("5:00")
    pace2 = Pace("6:00")
    assert pace2 >= pace1
    assert pace1 >= pace1


def test_less_than_or_equal():
    pace1 = Pace("5:00")
    pace2 = Pace("6:00")
    assert pace1 <= pace2
    assert pace1 <= pace1


@pytest.mark.parametrize(
    "min_per_km, expected_m_per_s",
    [
        (0.5, 33.333),  # 0:30 min/km (extremely fast)
        (0.6, 27.778),  # 0:36 min/km
        (0.7, 23.810),  # 0:42 min/km
        (1.0, 16.667),  # 1:00 min/km
        (1.1, 15.152),  # 1:06 min/km
        (1.2, 13.889),  # 1:12 min/km
        (1.3, 12.821),  # 1:18 min/km
        (5.0, 3.333),  # 5:00 min/km
        (5.5, 3.030),  # 5:30 min/km
        (6.0, 2.778),  # 6:00 min/km
        (10.0, 1.667),  # 10:00 min/km
        (10.5, 1.587),  # 10:30 min/km
    ],
)
def test_convert_pace_to_m_per_s(min_per_km, expected_m_per_s):
    result = Pace(min_per_km).to_m_per_s()
    assert result == pytest.approx(expected_m_per_s, rel=1e-3)


@pytest.mark.parametrize(
    "pace_str",
    [
        "0:30",
        "1:00",
        "5:00",
        "5:30",
        "15:30",
    ],
)
def test_convert_to_garmin(pace_str):
    pace = Pace("pace_str")
    assert pace.to_garmin() == pace.to_m_per_s()
