from flask import Blueprint
from .views import setup, login, logout

bp = Blueprint('auth', __name__, template_folder='templates', url_prefix="/auth",)
bp.add_url_rule("/setup",view_func=setup,methods=["GET","POST"])

bp.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
bp.add_url_rule("/logout", view_func=logout)

def init_app(app):
    app.register_blueprint(bp)
