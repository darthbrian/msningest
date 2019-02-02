from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
import uuid

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please user a different username.')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please user a different email address.')

class PostForm(FlaskForm):
    #uniqueid = StringField('Unique ID', validators=[DataRequired()])
    uniqueid = StringField('Unique ID', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    pubdate = DateField('Published Date', format='%Y-%m-%d', validators=[DataRequired()])
    videourl = StringField('Video URL', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

    #attribution = StringField('Copyright Information', validators=[DataRequired()])
    #thumbimg = StringField('Thumbnail Image', validators=[DataRequired()])
    #thumbatt = StringField('Thumbnail Copyright', validators=[DataRequired()])
    #vidlength = StringField('Video Length', validators=[DataRequired()])
    #update = StringField('Updated Date', validators=[DataRequired()])
    #weburl = StringField('Web URL', validators=[DataRequired()])
    #post = TextAreaField('Tags and Keywords', validators=[DataRequired(), Length(min=1, max=140)])

