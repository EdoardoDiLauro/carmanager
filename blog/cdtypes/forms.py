# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class CdTypeForm (FlaskForm) :
    name = StringField('Name',
                       validators=[DataRequired()])
    isperkm = RadioField('Distance Based', choices=[(0, 'No'), (1, 'Yes')], coerce=int,
                      validators=[DataRequired()])
    exgroup = SelectField(u'Add to extisting Cost Drivers group', coerce=int, validators=[Optional()])
    newgroup = StringField('Create new Cost Drivers group',
                       validators=[Optional()])
    submit = SubmitField('Add Cost Driver Type')
