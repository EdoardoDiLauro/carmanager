# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, DecimalField, SelectField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class CustomerForm (FlaskForm) :
    name = StringField('Name',
                        validators=[DataRequired()])
    address = StringField('Address',
                       validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Customer')
    submitup = SubmitField('Update Customer Details')

class UpdateCustomerForm (FlaskForm) :
    name = StringField('Name')
    address = StringField('Address')
    notes = TextAreaField('Notes')
    submitup = SubmitField('Update Customer Details')

class BindEventForm (FlaskForm) :
    evs = SelectField(u'Event', coerce=int, validators=[Optional()])
    submitev = SubmitField('Add Event to Customer')

