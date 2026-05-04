"""Integration tests for POST /activities/{activity_name}/signup endpoint."""
import pytest


def test_signup_success(client):
    """Test successful signup for an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_appends_participant(client):
    """Test that signing up adds the student to the activity's participants list."""
    # Arrange
    activity_name = "Programming Class"
    email = "newprogrammer@mergington.edu"
    
    # Get initial participants count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert signup_response.status_code == 200
    
    # Verify participant was added
    updated_response = client.get("/activities")
    updated_participants = updated_response.json()[activity_name]["participants"]
    assert len(updated_participants) == initial_count + 1
    assert email in updated_participants


def test_signup_duplicate_email_rejected(client):
    """Test that duplicate signup for the same activity is rejected."""
    # Arrange
    activity_name = "Gym Class"
    email = "duplicate@mergington.edu"

    # Act - First signup
    first_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Act - Second signup with same email
    second_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert - First succeeds, second is rejected
    assert first_response.status_code == 200
    assert second_response.status_code == 400

    # Verify error message
    error_data = second_response.json()
    assert "detail" in error_data
    assert "already signed up" in error_data["detail"].lower()

    # Verify participant was added only once
    final_response = client.get("/activities")
    participants = final_response.json()[activity_name]["participants"]
    duplicate_count = participants.count(email)
    assert duplicate_count == 1, "Duplicate email should appear only once"


def test_signup_activity_not_found(client):
    """Test that signing up for a non-existent activity returns 404."""
    # Arrange
    activity_name = "Non-Existent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_signup_missing_email_parameter(client):
    """Test that signup without email parameter is handled."""
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup"
    )

    # Assert
    # FastAPI should reject missing query parameter
    assert response.status_code == 422  # Unprocessable Entity


def test_signup_empty_email(client):
    """Test that signup with empty email string is handled."""
    # Arrange
    activity_name = "Chess Club"
    email = ""

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    # The endpoint accepts it currently, but we document the behavior
    # This could be enhanced with validation later
    assert response.status_code == 200
