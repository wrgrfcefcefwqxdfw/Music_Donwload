from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'peeeeeeepeeepoooopooo'
    # database is located sqlite:///DB_NAME
    # store this in the website folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # initialise database
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # The reason we import this is not because we're actually going to use anything. It is because
    # we need to make sure that we load  models.py file and that it runs and defines these classes before we initialize or create our database.
    # So we import the models file so that it defines these classes for us
    from .models import User, Note
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    # go to auth.login if you are not logged in
    login_manager.login_view = 'auth.login'
    # tell login manager which app we r using
    login_manager.init_app(app)

    # tell flask what user we r looking for
    @login_manager.user_loader
    def load_user(id):
        # similar to the filter_by
        # gets the primary key
        return User.query.get(int(id))
    return app
