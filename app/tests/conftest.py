import pytest
from flask_jwt_extended import create_access_token
from app import create_app, db, bcrypt
from app.models.user import User
from app.config import TestConfig

@pytest.fixture(scope='module')
def app():
    flask_app = create_app(TestConfig)

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def auth_headers(app):
    with app.app_context():
        hashed_pw = bcrypt.generate_password_hash('testpass').decode('utf-8')
        user = User(username='testuser', password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=str(user.id))
        return {
            'Authorization': f'Bearer {access_token}'
        }
