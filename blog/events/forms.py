# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class EventForm (FlaskForm) :
    start = DateField('Event Start',
                       validators=[DataRequired()], format='%Y-%m-%d')
    end = DateField('Event End',
                     validators=[DataRequired()], format='%Y-%m-%d')
    name = StringField('Name',
                        validators=[DataRequired()])
    kmssth = IntegerField('Forecasted SS Kms', validators=[Optional()])

    ccp = SelectField(u'Car Cost Profile', coerce=int, validators=[Optional()])

    submit = SubmitField('Add Event')

class UpdateEventForm (FlaskForm) :
    start = DateField('Event Start', format='%Y-%m-%d')
    end = DateField('Event End', format='%Y-%m-%d')
    name = StringField('Name')
    kmssth = IntegerField('Forecasted SS Kms', validators=[Optional()])
    ccp = SelectField(u'Car Cost Profile', coerce=int, validators=[Optional()])
    submit = SubmitField('Update Event')

