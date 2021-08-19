# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField, IntegerField, DecimalField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class InvoiceForm (FlaskForm) :
    regdate = DateField('Date',
                    validators=[DataRequired()], format='%Y-%m-%d')
    doc = FileField('Attached File (Allowed Extensions: txt, pdf, png, jpg, jpeg)')
    notes = TextAreaField('Notes')
    submit = SubmitField('Add New Invoice')