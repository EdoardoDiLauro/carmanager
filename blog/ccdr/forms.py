# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField, IntegerField, DecimalField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class CcdrForm (FlaskForm) :
    name = StringField('Name',
                       validators=[DataRequired()])
    notes = TextAreaField('Notes')

    submitccdr = SubmitField('Restore Cost Driver')