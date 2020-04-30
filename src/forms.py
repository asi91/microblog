from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from .models import User
from flask_login import current_user


class UserLogin(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember me")
    submit = SubmitField("submit")


class Registration(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    password2 = PasswordField("repeat password", validators=[DataRequired(), EqualTo("password")])
    email = StringField("email", validators=[DataRequired(), Email()])
    submit = SubmitField("register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Please use a different user name")

    def validate_email(self, email):
        user = User.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError("Please use a different email")


class AboutMe(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    about_me = TextAreaField("about me", validators=[Length(min=0, max=140)])
    submit = SubmitField("submit")

    def validate_username(self, username):
        if current_user.username == username.data:
            return
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Please use a different user name")
