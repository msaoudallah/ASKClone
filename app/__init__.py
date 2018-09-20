from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_gravatar import Gravatar
from flask_moment import Moment




db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
moment = Moment()
gravatar = Gravatar(
                    size=70,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)
    bootstrap.init_app(app)
    login.init_app(app)
    moment.init_app(app)
    gravatar.init_app(app)

    from app.errors import bp as errors_bp
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp,  url_prefix='/auth')
    app.register_blueprint(main_bp)

    return app


