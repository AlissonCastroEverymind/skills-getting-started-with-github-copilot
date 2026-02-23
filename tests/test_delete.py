"""Tests for the DELETE /activities/{activity_name}/signup endpoint."""

import pytest


def test_delete_participant_successful(client, test_activity):
    """Test successful removal of a participant from an activity."""
    # Get a participant from the activity
    activities_response = client.get("/activities")
    activities = activities_response.json()
    participant = activities[test_activity]["participants"][0]
    
    # Delete the participant
    response = client.delete(
        f"/activities/{test_activity}/signup?email={participant}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert participant in data["message"]


def test_delete_removes_participant_from_list(client, test_activity):
    """Test that deletion removes the email from participants list."""
    # Get initial participant list
    activities_response = client.get("/activities")
    activities = activities_response.json()
    participant = activities[test_activity]["participants"][0]
    initial_count = len(activities[test_activity]["participants"])
    
    # Delete participant
    response = client.delete(
        f"/activities/{test_activity}/signup?email={participant}"
    )
    assert response.status_code == 200
    
    # Verify removal
    final_response = client.get("/activities")
    final_data = final_response.json()
    final_count = len(final_data[test_activity]["participants"])
    
    assert final_count == initial_count - 1
    assert participant not in final_data[test_activity]["participants"]


def test_delete_nonexistent_activity_returns_404(client):
    """Test that deleting from nonexistent activity returns 404."""
    response = client.delete(
        "/activities/NonexistentActivity/signup?email=test@example.com"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_delete_not_signed_up_participant_returns_400(client, test_activity, test_email):
    """Test that deleting a non-participant returns 400 error."""
    response = client.delete(
        f"/activities/{test_activity}/signup?email={test_email}"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower() or "not found" in data["detail"].lower()


def test_delete_decrements_participant_count(client, test_activity):
    """Test that participant count decreases after deletion."""
    # Get a participant
    activities_response = client.get("/activities")
    activities = activities_response.json()
    participant = activities[test_activity]["participants"][0]
    initial_count = len(activities[test_activity]["participants"])
    
    # Delete
    response = client.delete(
        f"/activities/{test_activity}/signup?email={participant}"
    )
    assert response.status_code == 200
    
    # Verify count decreased
    final_response = client.get("/activities")
    final_data = final_response.json()
    final_count = len(final_data[test_activity]["participants"])
    
    assert final_count == initial_count - 1


def test_delete_then_signup_same_email(client, test_activity, test_email):
    """Test that an email can be added again after deletion."""
    # Sign up
    response1 = client.post(
        f"/activities/{test_activity}/signup?email={test_email}"
    )
    assert response1.status_code == 200
    
    # Delete
    response2 = client.delete(
        f"/activities/{test_activity}/signup?email={test_email}"
    )
    assert response2.status_code == 200
    
    # Sign up again
    response3 = client.post(
        f"/activities/{test_activity}/signup?email={test_email}"
    )
    assert response3.status_code == 200
    
    # Verify in participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert test_email in activities[test_activity]["participants"]


def test_delete_multiple_participants_separately(client, test_activity):
    """Test deleting multiple participants one by one."""
    # Get initial participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    initial_participants = activities[test_activity]["participants"].copy()
    initial_count = len(initial_participants)
    
    # Delete first participant
    response1 = client.delete(
        f"/activities/{test_activity}/signup?email={initial_participants[0]}"
    )
    assert response1.status_code == 200
    
    # Delete second participant
    response2 = client.delete(
        f"/activities/{test_activity}/signup?email={initial_participants[1]}"
    )
    assert response2.status_code == 200
    
    # Verify both removed
    final_response = client.get("/activities")
    final_data = final_response.json()
    final_count = len(final_data[test_activity]["participants"])
    
    assert final_count == initial_count - 2
    assert initial_participants[0] not in final_data[test_activity]["participants"]
    assert initial_participants[1] not in final_data[test_activity]["participants"]
