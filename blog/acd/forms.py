# coding=utf-8
from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, DecimalField, FieldList, FormField, HiddenField, RadioField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class AcdForm (FlaskForm) :
    name = StringField('Name',
                        validators=[DataRequired()])
    value = IntegerField('Forecasted Cost',
                         validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Activity Cost Driver')

class UpdateAcdForm (FlaskForm) :
    name = StringField('Name',
                        validators=[DataRequired()])
    value = IntegerField('Forecasted Cost',
                         validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Update Activity Cost Driver')

class UpdateAcdFormDash (FlaskForm) :
    cdid = HiddenField()
    name = StringField('Name',
                        validators=[DataRequired()])
    value = IntegerField('Forecasted Cost',
                         validators=[DataRequired()])
    notes = TextAreaField('Notes')

class AcdDashForm (Form):
    cds = FieldList(FormField(UpdateAcdFormDash))
    submit = SubmitField('Update Activity Cost Drivers')


