"""Pytest configuration and fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient instance for testing the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """Provide a fresh activities dictionary for isolated test data."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Join our competitive basketball team for practice and games",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Improve your tennis skills and compete in matches",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["jessica@mergington.edu", "david@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 8,
            "participants": ["maria@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore various art mediums and techniques",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["lucas@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["ryan@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design and build robots for competitions",
            "schedule": "Fridays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["chris@mergington.edu", "nora@mergington.edu"]
        }
    }


@pytest.fixture(autouse=True)
def reset_activities(fresh_activities):
    """Reset activities to fresh state before each test."""
    activities.clear()
    activities.update(fresh_activities)
    yield
    activities.clear()
    activities.update(fresh_activities)


@pytest.fixture
def test_email():
    """Provide a test email address."""
    return "test.student@mergington.edu"


@pytest.fixture
def test_activity():
    """Provide a test activity name."""
    return "Chess Club"
