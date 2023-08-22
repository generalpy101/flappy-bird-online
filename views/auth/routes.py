from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from .forms import LoginForm, RegistrationForm
from models.user import User
from models import db

auth_bp = Blueprint("auth", __name__, template_folder="templates")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # You need to retrieve the user based on the provided username
        # and validate the password. Replace this part with your actual logic.
        user = User.query.filter_by(name=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            next_page = request.args.get("next")

            if not next_page:
                if user.is_admin:
                    next_page = url_for("admin.list_lobbies")
                else:
                    next_page = url_for("player.join_lobby")
            return redirect(next_page or url_for("index"))
        else:
            flash("Login failed. Please check your credentials.", "error")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(name=form.name.data)
        new_user.password = form.password.data
        # Check if username already exists
        if User.query.filter_by(name=form.name.data).first():
            flash("Username already exists.", "error")
            return redirect(url_for("auth.register"))
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
