# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class CarForm (FlaskForm) :
    brand = StringField('Brand',
                        validators=[DataRequired()])
    model = StringField('Model',
                        validators=[DataRequired()])
    group = StringField('Group',
                        validators=[DataRequired()])
    cat = StringField('Class',
                        validators=[DataRequired()])
    plate = StringField('License Plate (optional)')
    submit = SubmitField('Add Car')

