from flask import render_template, request, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from loja.ext.database import db
from loja.model import User
from flask_login import login_user, logout_user

def has_users():
    return db.session.execute(db.select(User.id).limit(1)).first() is not None

def setup():
    if has_users():
        abort(404)

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        confirm = request.form["confirm"]

        if not username or not password:
            flash("Informe um usuário e uma senha.")
        elif password != confirm:
            flash("As senhas não conferem.")
        else:
            db.session.add(User(
                username=username,
                password_hash=generate_password_hash(password),
                is_admin=True,
            ))
            db.session.commit()
            return redirect(url_for("auth.login"))

    return render_template("setup.html")

def login():
    if not has_users():
        return redirect(url_for("auth.setup"))

    if request.method == "POST":
        user = db.session.execute(
            db.select(User).filter_by(username=request.form["username"].strip())
        ).scalar()

        if user and check_password_hash(user.password_hash, request.form["password"]):
            login_user(user)
            next_url = request.args.get("next", "")
            if next_url.startswith("/") and not next_url.startswith(("//", "/\\")):
                return redirect(next_url)
            return redirect(url_for("admin.index"))

        flash("Usuário ou senha inválidos.")

    return render_template("login.html")


def logout():
    logout_user()
    return redirect(url_for("auth.login"))
