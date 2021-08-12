# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class CarForm (FlaskForm) :
    brand = StringField('Brand',
                        validators=[DataRequired()])
    model = StringField('Model',
                        validators=[DataRequired()])
    kmtot = IntegerField('Total Kms of SS',
                        validators=[DataRequired()])
    chassis = StringField('Chassis Number',
                        validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Car')

class UpdateCarForm (FlaskForm) :
    brand = StringField('Brand',
                        validators=[DataRequired()])
    model = StringField('Model',
                        validators=[DataRequired()])
    kmtot = IntegerField('Total Kms of SS',
                        validators=[DataRequired()])
    chassis = StringField('Chassis Number',
                        validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Update Car')
