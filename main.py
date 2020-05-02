from src.app import app, db
from src.models import Post, User


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Post": Post, "User": User}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
