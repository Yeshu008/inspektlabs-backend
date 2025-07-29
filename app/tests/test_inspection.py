from flask_jwt_extended import create_access_token
from app import db,bcrypt
from app.models.user import User
def create_inspection_for_user(client, auth_headers):
    response = client.post('/inspection', json={
        "vehicle_number": "DL01AB1234",
        "damage_report": "Scratch",
        "image_url": "https://example.com/image.jpg"
    }, headers=auth_headers)

    assert response.status_code == 201

def create_inspection_for_user(client, token):
    response = client.post(
        "/inspection",
        json={
            "vehicle_number": "DL01AB1234",
            "damage_report": "Test damage",
            "image_url": "https://example.com/image.jpg",
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    print("RESPONSE STATUS:", response.status_code)
    print("RESPONSE JSON:", response.get_json())
    return response.get_json()["id"]

def test_create_inspection_invalid_image(client, auth_headers):
    response = client.post('/inspection', json={
        "vehicle_number": "DL01AB1234",
        "damage_report": "Scratch Bumper",
        "image_url": "https://example.com/image.txt"
    }, headers=auth_headers)
    assert response.status_code == 400

def test_get_own_inspection(client, auth_headers):
    token = auth_headers["Authorization"].split(" ")[1]
    inspection_id = create_inspection_for_user(client,token)
    response2 = client.get(f"/inspection/{inspection_id}", headers=auth_headers)
    assert response2.status_code == 200
    assert "vehicle_number" in response2.json

def test_get_other_user_inspection(client, app):
    with app.app_context():
        hashed_pw = bcrypt.generate_password_hash('user100pass').decode('utf-8')
        user1 = User(username='user100', password_hash=hashed_pw)
        db.session.add(user1)

        hashed_pw2 = bcrypt.generate_password_hash('user200pass').decode('utf-8')
        user2 = User(username='user200', password_hash=hashed_pw2)
        db.session.add(user2)

        db.session.commit()
        token1 = create_access_token(identity=str(user1.id))
        token2 = create_access_token(identity=str(user2.id))

    inspection_id = create_inspection_for_user(client, token1)

    response = client.get(f"/inspection/{inspection_id}", headers={"Authorization": f"Bearer {token2}"})
    assert response.status_code == 403

def test_patch_inspection_status(client, auth_headers):
    token = auth_headers["Authorization"].split(" ")[1]
    inspection_id = create_inspection_for_user(client, token)
    response = client.patch(f"/inspection/{inspection_id}", json={"status": "reviewed"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json["message"] == "Status updated"

def test_patch_invalid_status(client, auth_headers):
    token = auth_headers["Authorization"].split(" ")[1]
    inspection_id = create_inspection_for_user(client, token)
    response = client.patch(f"/inspection/{inspection_id}", json={"status": "invalid"}, headers=auth_headers)
    assert response.status_code == 400

def test_filter_by_status(client, auth_headers):
    token = auth_headers["Authorization"].split(" ")[1]
    create_inspection_for_user(client, token)
    response = client.get("/inspection?status=pending", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)