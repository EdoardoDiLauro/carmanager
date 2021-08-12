# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, DecimalField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class CcdForm (FlaskForm) :
    name = StringField('Name',
                        validators=[DataRequired()])
    value = IntegerField('Forecasted Absolute Cost',
                         validators=[DataRequired()])
    elapsed = DecimalField('Component Elapsed Life (set 0 if new)',
                         validators=[DataRequired()])
    limit = IntegerField('Forecasted Component Life',
                         validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Car Cost Driver')