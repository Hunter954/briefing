import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "admin.login"
login_manager.login_message = "Faça login para acessar o painel."
login_manager.login_message_category = "warning"


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    database_url = os.getenv("DATABASE_URL", "sqlite:///briefings.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://") and "+" not in database_url.split("://", 1)[0]:
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    max_mb = int(os.getenv("MAX_CONTENT_LENGTH_MB", "30"))

    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret-key"),
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_ROOT=os.getenv("UPLOAD_ROOT", "/data/uploads"),
        MAX_CONTENT_LENGTH=max_mb * 1024 * 1024,
    )

    os.makedirs(os.path.join(app.config["UPLOAD_ROOT"], "reference_images"), exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import User, Briefing, OptionValue, ReferenceImage

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.public.routes import public_bp
    from app.admin.routes import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    return app
