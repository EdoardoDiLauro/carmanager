# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, DecimalField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class CustomerForm (FlaskForm) :
    name = StringField('Name',
                        validators=[DataRequired()])
    address = StringField('Name',
                       validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Customer')