def test_signup_success(client):
    response = client.post('/signup', json={"username": "user1", "password": "securepass"})
    assert response.status_code == 201

def test_login_invalid_user(client):
    response = client.post('/login', json={"username": "nouser", "password": "pass"})
    assert response.status_code == 401
