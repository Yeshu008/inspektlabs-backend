from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from app.config import Config
from app.utils.logger import setup_logging
from app.errors.jwt_errors import register_jwt_callbacks

db = SQLAlchemy()
jwt = JWTManager()
bcrypt =Bcrypt()

def create_app(config_file=Config):
    app = Flask(__name__)
    app.config.from_object(config_file)

    setup_logging(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    register_jwt_callbacks(jwt)
    bcrypt.init_app(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.main_routes import main_bp
    from app.routes.inspection_routes import inspection_bp
    from app.errors.errors import error_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(inspection_bp)
    app.register_blueprint(error_bp)

    return app
