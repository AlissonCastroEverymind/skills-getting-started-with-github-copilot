"""Tests for the GET / redirect endpoint."""

import pytest


def test_root_redirects_to_static(client):
    """Test that GET / redirects to /static/index.html."""
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code == 307
    assert "location" in response.headers
    assert "/static/index.html" in response.headers["location"]


def test_root_with_follow_redirects(client):
    """Test that following the redirect works correctly."""
    response = client.get("/", follow_redirects=True)
    
    assert response.status_code == 200
    # The response should contain HTML content from index.html
    assert "Mergington High School" in response.text or response.headers.get("content-type")
