# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class EventForm (FlaskForm) :
    type = RadioField('Type', choices=[(0, 'Test'), (1, 'Race'), (2, 'Restore')], coerce=int,
                      validators=[DataRequired()])
    start = DateField('Car Busy',
                       validators=[DataRequired()], format='%Y-%m-%d')
    end = DateField('Car Free',
                     validators=[DataRequired()], format='%Y-%m-%d')
    name = StringField('Name',
                        validators=[DataRequired()])
    year = StringField('Year',
                        validators=[DataRequired()])
    kms = IntegerField('SS Kms', validators=[Optional()])

    submit = SubmitField('Add Activity')

class UpdateEventForm (FlaskForm) :
    type = RadioField('Type', choices=[(0, 'Test'), (1, 'Race'), (2, 'Restore')], coerce=int,
                      validators=[DataRequired()])
    start = DateField('Car Busy',
                       validators=[DataRequired()])
    end = DateField('Car Free',
                     validators=[DataRequired()])
    name = StringField('Name',
                        validators=[DataRequired()])
    year = StringField('Year',
                        validators=[DataRequired()])
    kms = IntegerField('SS Kms', validators=[Optional()])

    submit = SubmitField('Update Activity')

class AddCarForm(FlaskForm):
    car = SelectField(u'Car', coerce=int, validators=[Optional()])
    team = SelectField(u'Team', coerce=int, validators=[Optional()])
    submit = SubmitField('Assign Car')