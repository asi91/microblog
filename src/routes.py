from .app import app, db
from flask import render_template, redirect, flash, url_for, request
from .forms import UserLogin, Registration, AboutMe
from flask_login import current_user, login_user, logout_user, login_required
from .models import User
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            "author": {"username": "John Legend"},
            "body": "I am legend"
        },
        {
            "author": {"username": "Hamza Assi"},
            "body": "I am Python Developer"
        }
    ]
    return render_template("index.html", title="Humble Blog Homepage", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = Registration()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = UserLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(f"Invalid user name or password, please try again")
            return redirect(url_for("register"))
        login_user(user, remember=form.remember_me.data)
        redirect_page = request.args.get("next")
        if not redirect_page or url_parse(redirect_page).netloc != "":
            redirect_page = url_for("index")

        return redirect(redirect_page)

    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/user/<username>")
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {
            "author": user,
            "body": "I am legend"
        },
        {
            "author": user,
            "body": "I am Python Developer"
        }
    ]
    return render_template("user_profile.html", user=user, posts=posts)


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = AboutMe()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for("user_profile", username=current_user.username))
    elif request.method == "GET":
        current_user.username = form.username
        current_user.about_me = form.about_me

    return render_template("edit_profile.html", title="Edit Profile", form=form)
