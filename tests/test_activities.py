"""Tests for the GET /activities endpoint."""

import pytest


def test_get_activities_returns_200(client):
    """Test that GET /activities returns a 200 status code."""
    response = client.get("/activities")
    assert response.status_code == 200


def test_get_activities_returns_dict(client):
    """Test that GET /activities returns a dictionary."""
    response = client.get("/activities")
    data = response.json()
    assert isinstance(data, dict)


def test_get_activities_contains_all_default_activities(client):
    """Test that all default activities are present in the response."""
    response = client.get("/activities")
    data = response.json()
    
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Debate Team",
        "Art Club",
        "Science Club",
        "Robotics Club"
    ]
    
    for activity in expected_activities:
        assert activity in data


def test_activity_has_required_fields(client):
    """Test that each activity has all required fields."""
    response = client.get("/activities")
    data = response.json()
    
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for activity_name, activity_details in data.items():
        for field in required_fields:
            assert field in activity_details, f"Missing '{field}' in {activity_name}"


def test_activity_participants_is_list(client):
    """Test that participants field is a list."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_details in data.items():
        assert isinstance(activity_details["participants"], list)


def test_activity_max_participants_is_int(client):
    """Test that max_participants is an integer."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_details in data.items():
        assert isinstance(activity_details["max_participants"], int)
        assert activity_details["max_participants"] > 0


def test_all_participants_are_emails(client):
    """Test that all participants are valid email-like strings."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_details in data.items():
        for participant in activity_details["participants"]:
            assert "@" in participant and "." in participant
