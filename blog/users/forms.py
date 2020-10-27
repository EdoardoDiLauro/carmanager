from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, RadioField, FormField, FieldList
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_login import current_user
from blog.models import User


class RegistrationForm (FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired()])
    email = StringField('Email',
                          validators=[DataRequired(), Email()])
    name = StringField('Name',
                           validators=[DataRequired()])
    surname = StringField('Surname',
                           validators=[DataRequired()])
    password = PasswordField('Password',
                          validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign In')

    def validate_username(self, username):
        race = User.query.filter_by(username=username.data).first()
        if race:
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        race = User.query.filter_by(email=email.data).first()
        if race:
            raise ValidationError('Email already in use, please follow password recovery procedure')



class LoginForm (FlaskForm) :

    email = StringField('Email',
                          validators=[DataRequired(), Email()])
    password= PasswordField('Password',
                          validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UpdateAccountForm (FlaskForm) :
    username = StringField('Username',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    name = StringField('Name',
                       validators=[DataRequired()])
    surname = StringField('Surname',
                          validators=[DataRequired()])
    picture = FileField('Profile Picture (allowed extensions: .jpg, .png)', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        race = User.query.filter_by(username=username.data).first()
        if race:
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        race = User.query.filter_by(email=email.data).first()
        if race:
            raise ValidationError('Email already in use, please follow password recovery procedure')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Password Reset Request')

    def validate_email(self, email):
        race = User.query.filter_by(email=email.data).first()
        if race is None:
            raise ValidationError('Unknown mail address')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class ContactForm(FlaskForm):
    subject = StringField('Subject',
                           validators=[DataRequired()])

    body = TextAreaField ('Body',
                           validators=[DataRequired()])

    submit = SubmitField('Send')

class UserForm(FlaskForm):
    rid= IntegerField()
    status=StringField()
    nome=StringField()
    onhold = RadioField('', choices=[(0, 'Yes'),(1, 'No')], coerce=int, validators=[Optional()])

class UserValidationForm(Form):
    users = FieldList(FormField(UserForm))
    submit=SubmitField('Validate Users')
