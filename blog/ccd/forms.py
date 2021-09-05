# coding=utf-8
from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField, IntegerField, DecimalField, \
    FieldList, FormField, HiddenField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class CcdForm (FlaskForm) :
    name = StringField('Name',
                        validators=[DataRequired()])
    value = IntegerField('Forecasted Absolute Cost',
                         validators=[DataRequired()])
    elapsed = DecimalField('Component Elapsed Life (set 0 if new)')
    limit = IntegerField('Forecasted Component Life',
                         validators=[DataRequired()])
    submitccdnew = SubmitField('Add Car Cost Driver')

class UpdateCcdForm (FlaskForm) :
    name = StringField('Name',
                        validators=[DataRequired()])
    value = IntegerField('Forecasted Absolute Cost',
                         validators=[DataRequired()])
    elapsed = DecimalField('Component Elapsed Life (set 0 if new)')
    avg = DecimalField('Component Average Life',
                           validators=[DataRequired()])
    limit = IntegerField('Forecasted Component Life',
                         validators=[DataRequired()])
    submit = SubmitField('Update Car Cost Driver')

class CcdFormDash (FlaskForm) :
    spid = HiddenField()
    select = RadioField('', choices=[(1, ' '), (0, 'No')], coerce=int, validators=[Optional()])
    nome = StringField('Name',
                       validators=[DataRequired()])
    value = IntegerField('Forecasted Absolute Cost',
                         validators=[DataRequired()])
    elapsed = DecimalField('Component Elapsed Life (set 0 if new)',
                           validators=[DataRequired()])
    avg = DecimalField('Component Average Life',
                       validators=[DataRequired()])
    limit = IntegerField('Forecasted Component Life',
                         validators=[DataRequired()])

class CcdDashForm (Form):
    sps = FieldList(FormField(CcdFormDash))
    submitin = SubmitField('Assign Selected Cost Drivers')
    submitoff = SubmitField('Discard Selected Cost Drivers')
    submitres = SubmitField('Restore Cost Driver')