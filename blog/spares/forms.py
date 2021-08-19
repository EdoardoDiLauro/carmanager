# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField, IntegerField, DecimalField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class SpareForm (FlaskForm) :
    area = StringField('Area',
                       validators=[DataRequired()])
    name = StringField('Name',
                        validators=[DataRequired()])
    isnew = RadioField('', choices=[(1, 'Yes'), (0, 'No')], coerce=int, validators=[Optional()])
    price = DecimalField('Price',
                        validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Spare Part')