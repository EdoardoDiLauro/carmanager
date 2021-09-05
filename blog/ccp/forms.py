# coding=utf-8
from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField, IntegerField, DecimalField, \
    FieldList, FormField, HiddenField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class CcpForm (FlaskForm) :
    name = StringField('Name',
                        validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Car Cost Profile')

class UpdateCcpForm (FlaskForm) :
    name = StringField('Name')
    notes = TextAreaField('Notes')
    submitupccp = SubmitField('Update Car Cost Profile')

