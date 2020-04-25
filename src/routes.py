from .app import app
from flask import render_template, redirect, flash, url_for
from .forms import UserLogin


@app.route('/')
@app.route('/index')
def index():
    users = {"username": "Hamza"}
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
    return render_template("index.html", title="Humble Blog Homepage", user=users, posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = UserLogin()
    if form.validate_on_submit():
        flash(f"Login requested for user `{form.username.data}`, remember me={form.remember_me.data}")
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)
