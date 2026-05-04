"""Integration tests for GET /activities endpoint."""
import pytest


def test_get_activities_success(client):
    """Test that GET /activities returns all activities successfully."""
    # Arrange
    # client fixture is already prepared

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0


def test_get_activities_structure(client, sample_activities):
    """Test that GET /activities returns correct data structure."""
    # Arrange
    expected_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert isinstance(activity_data, dict)
        assert expected_keys.issubset(activity_data.keys())
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_get_activities_includes_participants(client, sample_activities):
    """Test that GET /activities includes the participants list populated."""
    # Arrange
    # Activities already have participants in the app

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    # At least one activity should have participants
    activities_with_participants = [
        activity for activity in activities.values()
        if len(activity["participants"]) > 0
    ]
    assert len(activities_with_participants) > 0
    # Verify participants are email strings
    for activity in activities_with_participants:
        for participant in activity["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email format check
