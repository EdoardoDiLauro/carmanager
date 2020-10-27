# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField, IntegerField, DecimalField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class CdForm (FlaskForm) :
    name = StringField('Name',
                        validators=[DataRequired()])
    qty = IntegerField('Quantity (if Cost Driver is NOT distance based)',
                       validators=[Optional()])
    uncost = DecimalField('Unit/Km Cost',
                       validators=[DataRequired()])
    type = SelectField(u'Type', coerce=int, validators=[Optional()])

    submit = SubmitField('Add Cost Driver')
