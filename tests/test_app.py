from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Expect activities dict to contain at least one known activity
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "pytest-temp@example.com"

    # Ensure clean state for this test email
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Remove
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]


def test_remove_nonexistent_participant_returns_404():
    activity = "Chess Club"
    email = "definitely-not-registered@example.com"

    # Make sure the email is not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 404
