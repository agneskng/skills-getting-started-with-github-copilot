from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: No special setup needed as activities are predefined
    
    # Act: Make the GET request
    response = client.get("/activities")
    
    # Assert: Check status and structure
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    for activity_name, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)

def test_signup_success():
    # Arrange: Choose an activity and email
    activity = "Chess Club"
    email = "test@mergington.edu"
    
    # Act: Sign up the participant
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Check success response and that participant was added
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    
    # Verify in activities data
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity]["participants"]

def test_signup_duplicate():
    # Arrange: Sign up once first
    activity = "Chess Club"
    email = "duplicate@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Act: Try to sign up again
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Should fail with duplicate error
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    # Arrange: Use a non-existent activity
    invalid_activity = "Invalid Activity"
    email = "test@mergington.edu"
    
    # Act: Attempt signup
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert: Should return 404
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_delete_participant_success():
    # Arrange: Add a participant first
    activity = "Programming Class"
    email = "delete@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Act: Delete the participant
    response = client.delete(f"/activities/{activity}/participants/{email}")
    
    # Assert: Check success and that participant was removed
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]
    
    # Verify removal
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities[activity]["participants"]

def test_delete_participant_not_signed_up():
    # Arrange: Use an email not signed up
    activity = "Chess Club"
    email = "notsigned@mergington.edu"
    
    # Act: Try to delete
    response = client.delete(f"/activities/{activity}/participants/{email}")
    
    # Assert: Should return 404
    assert response.status_code == 404
    data = response.json()
    assert "not signed up" in data["detail"]

def test_delete_invalid_activity():
    # Arrange: Use invalid activity
    invalid_activity = "Invalid Activity"
    email = "test@mergington.edu"
    
    # Act: Attempt delete
    response = client.delete(f"/activities/{invalid_activity}/participants/{email}")
    
    # Assert: Should return 404
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]