import pytest
from garminworkouts.models.distance import Distance


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("400 meters", 400.0),
        ("400 m", 400.0),
        ("400M", 400.0),
        ("400 M", 400.0),
        ("5.5 km", 5500.0),
        ("21 kilometers", 21000.0),
    ],
)
def test_valid_distances(input_str, expected):
    d = Distance(input_str)
    assert d.distance_meters == expected


@pytest.mark.parametrize(
    "input_str",
    [
        "100 yards",
        "five hundred meters",
    ],
)
def test_invalid_distances(input_str):
    with pytest.raises(ValueError):
        Distance(input_str)
