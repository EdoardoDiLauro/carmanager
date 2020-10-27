# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class TeamForm (FlaskForm) :
    name = StringField('Name',
                        validators=[DataRequired()])
    submit = SubmitField('Add Team')

class AddCarForm(FlaskForm):
    car = SelectField(u'Car', coerce=int, validators=[Optional()])
    submit = SubmitField('Assign Car')
