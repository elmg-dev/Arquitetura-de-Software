from flask import redirect, url_for, request, abort, flash
from flask_login import current_user
from flask_babel import Babel
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from loja.ext.database import db
from loja.ext.login import has_users
from loja.model import Product, User
from werkzeug.security import generate_password_hash
from wtforms import PasswordField, ValidationError


class AdminAccessMixin:
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        if not has_users():
            return redirect(url_for("auth.setup"))
        if current_user.is_authenticated:
            abort(403)  # logado, mas não é admin
        return redirect(url_for("auth.login", next=request.path))


class SecureAdminIndexView(AdminAccessMixin, AdminIndexView):
    pass


class SecureModelView(AdminAccessMixin, ModelView):
    pass

 
class UserModelView(SecureModelView):
    """Cadastro de usuários: a senha digitada nunca é gravada, só o hash."""

    column_list = ["username", "is_admin"]
    form_columns = ["username", "password", "is_admin"]
    form_extra_fields = {"password": PasswordField("Senha")}

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password_hash = generate_password_hash(form.password.data)
        elif is_created:
            raise ValidationError("Informe uma senha para o novo usuário.")

    def delete_model(self, model):
        if model.id == current_user.id:
            flash("Você não pode excluir o usuário logado.", "warning")
            return False
        return super().delete_model(model)


def init_app(app):
     babel = Babel(app)
     admin = Admin(app, index_view=SecureAdminIndexView())
     admin.add_view(SecureModelView(Product, db.session))
     admin.add_view(UserModelView(User, db.session, name="Usuários"))
