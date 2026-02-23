"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


def test_signup_successful(client, test_activity, test_email):
    """Test successful signup for an activity."""
    response = client.post(
        f"/activities/{test_activity}/signup?email={test_email}",
        follow_redirects=False
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert test_activity in data["message"]


def test_signup_adds_participant_to_activity(client, test_activity, test_email):
    """Test that signup adds the email to participants list."""
    response = client.post(
        f"/activities/{test_activity}/signup?email={test_email}"
    )
    
    assert response.status_code == 200
    
    # Verify by fetching activities
    activities_response = client.get("/activities")
    activities = activities_response.json()
    
    assert test_email in activities[test_activity]["participants"]


def test_signup_duplicate_returns_400(client, test_activity, test_email):
    """Test that signing up twice for same activity returns 400 error."""
    # First signup
    response1 = client.post(
        f"/activities/{test_activity}/signup?email={test_email}"
    )
    assert response1.status_code == 200
    
    # Duplicate signup
    response2 = client.post(
        f"/activities/{test_activity}/signup?email={test_email}"
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower() or "duplicate" in data["detail"].lower()


def test_signup_nonexistent_activity_returns_404(client, test_email):
    """Test that signing up for a nonexistent activity returns 404."""
    response = client.post(
        "/activities/NonexistentActivity/signup?email=test@example.com"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_increments_participant_count(client, test_activity, test_email):
    """Test that participant count increases after signup."""
    # Get initial count
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    initial_count = len(initial_data[test_activity]["participants"])
    
    # Sign up
    response = client.post(
        f"/activities/{test_activity}/signup?email={test_email}"
    )
    assert response.status_code == 200
    
    # Get new count
    final_response = client.get("/activities")
    final_data = final_response.json()
    final_count = len(final_data[test_activity]["participants"])
    
    assert final_count == initial_count + 1


def test_signup_email_case_sensitivity(client, test_activity):
    """Test signup with different email formats."""
    email1 = "student@mergington.edu"
    email2 = "STUDENT@mergington.edu"
    
    response1 = client.post(
        f"/activities/{test_activity}/signup?email={email1}"
    )
    assert response1.status_code == 200
    
    # Different case should be treated as different email
    response2 = client.post(
        f"/activities/{test_activity}/signup?email={email2}"
    )
    # This will succeed since emails are case-sensitive in current implementation
    assert response2.status_code == 200


def test_signup_with_special_characters_in_email(client, test_activity):
    """Test signup with special characters in email (URL encoded)."""
    import urllib.parse
    
    email = "student+test@mergington.edu"
    encoded_email = urllib.parse.quote(email, safe='')
    
    response = client.post(
        f"/activities/{test_activity}/signup?email={encoded_email}"
    )
    
    assert response.status_code == 200
    
    # Verify in participants with URL-decoded format
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[test_activity]["participants"]
