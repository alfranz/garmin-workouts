import pytest
from unittest.mock import Mock, patch
from garminworkouts.garmin.garminclient import (
    GarminClient,
    GarminException,
)


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("GARMIN_USERNAME", "test_user")
    monkeypatch.setenv("GARMIN_PASSWORD", "test_password")


@pytest.fixture
def garmin_client():
    with patch("garth.Client") as mock_garth_client:
        mock_garth_client.return_value.connectapi = Mock()
        return GarminClient()


def test_init_missing_username(monkeypatch):
    monkeypatch.delenv("GARMIN_USERNAME", raising=False)
    with pytest.raises(GarminException) as excinfo:
        GarminClient(password="test_password")
    assert "Username is required" in str(excinfo.value)


def test_init_missing_password(monkeypatch):
    monkeypatch.delenv("GARMIN_PASSWORD", raising=False)
    with pytest.raises(GarminException) as excinfo:
        GarminClient(username="test_user")
    assert "Password is required" in str(excinfo.value)
