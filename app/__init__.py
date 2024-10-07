from flask import Flask
from app.config import Config, configure_logging
from .views import webhook_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load configurations and logging settings
    app.config.from_object(Config)
    configure_logging()


    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints, if any
    app.register_blueprint(webhook_blueprint)

    from app.models import models

    @app.shell_context_processor
    def make_shell_context():
        from app.models.models import User, TrainingSession, TrainingDetail  # Importa tus modelos aquí
        import sqlalchemy as sa
        import sqlalchemy.orm as so 
        return {
            'db': db,
            'User': User,
            'TrainingSession': TrainingSession,
            'TrainingDetail': TrainingDetail,
            'sa': sa, 
            'so': so,
        }
    
    return app
