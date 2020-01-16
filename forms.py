from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length


class RegistrationForm():
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('Confirm Password')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm():
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')
