# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class AcpForm (FlaskForm) :
    name = StringField('Name',
                        validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submitacp = SubmitField('Add Activity Cost Profile')

class UpdateAcpForm (FlaskForm) :
    name = StringField('Name')
    notes = TextAreaField('Notes')
    submitacpup = SubmitField('Update Activity Cost Profile')