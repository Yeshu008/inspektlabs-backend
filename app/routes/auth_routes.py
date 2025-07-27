from flask import Blueprint, request, jsonify,abort
from app import db,bcrypt
from app.models.user import User
from app.utils.logger import logger
from werkzeug.exceptions import HTTPException
from app.schemas.user_schema import SignupSchema,LoginSchema
from pydantic import ValidationError
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,create_refresh_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        payload = SignupSchema(**request.get_json())
    except ValidationError as e:
        abort(400, description=e.errors())

    username = payload.username
    password = payload.password

    if User.query.filter_by(username=username).first():
        abort(400,description='Username already exists')

    try:
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password_hash=hashed)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created'}), 201
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"[SIGNUP_FAILURE] User: {username} - {str(e)}")

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        payload = LoginSchema(**request.get_json())
    except ValidationError as e:
        abort(400, description=e.errors())
    username = payload.username
    password = payload.password

    try:
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            return jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        abort(401, description='Invalid credentials')
    except HTTPException:
        raise
    except Exception as e:
        abort(500, description=f"[LOGIN_FAILURE] User: {username} - {str(e)}")
    
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token), 200
