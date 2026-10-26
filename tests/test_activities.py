def test_get_activities_returns_activity_details(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert {
        "description",
        "schedule",
        "max_participants",
        "participants",
    } <= activities["Chess Club"].keys()


def test_signup_adds_participant(client):
    email = "new-student@mergington.edu"

    response = client.post(
        "/activities/Basketball Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email in client.get("/activities").json()["Basketball Club"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    email = "new-student@mergington.edu"
    url = "/activities/Basketball Club/signup"
    client.post(url, params={"email": email})

    response = client.post(url, params={"email": email})

    assert response.status_code == 400
    participants = client.get("/activities").json()["Basketball Club"]["participants"]
    assert participants.count(email) == 1


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404


def test_delete_signup_removes_participant(client):
    email = "michael@mergington.edu"

    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]


def test_delete_signup_returns_404_for_unregistered_email(client):
    response = client.delete(
        "/activities/Basketball Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404


def test_delete_signup_returns_404_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404