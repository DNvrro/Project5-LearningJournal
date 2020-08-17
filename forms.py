from flask_wtf import Form
from wtforms import (StringField, PasswordField, TextAreaField, IntegerField, DateField)
from wtforms.validators import (DataRequired, ValidationError, Email, Length, EqualTo, Regexp)

from models import UserMixin, User


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')

class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                        "numbers, and underscores only.")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class EntryForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time_spent = IntegerField('Time Spent', validators=[DataRequired()])
    what_i_learned = TextAreaField('What I Learned', validators=[DataRequired()])
    resources_to_remember = TextAreaField('Resources to Remember', validators=[DataRequired()])

class EditEntryForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time_spent = IntegerField('Time Spent', validators=[DataRequired()])
    what_i_learned = TextAreaField('What I Learned', validators=[DataRequired()])
    resources_to_remember = TextAreaField('Resources to Remember', validators=[DataRequired()])

