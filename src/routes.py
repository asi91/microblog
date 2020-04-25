from .app import app
from flask import render_template


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
