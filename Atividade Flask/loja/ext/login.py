from flask_login import LoginManager
from loja.ext.database import db
from loja.model import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def has_users():
    return db.session.execute(db.select(User.id).limit(1)).first() is not None


def init_app(app):
    login_manager.init_app(app)
