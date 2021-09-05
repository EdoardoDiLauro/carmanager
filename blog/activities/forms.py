# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField, IntegerField, DecimalField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class ActForm (FlaskForm) :
    start = DateTimeLocalField('Activity Start',
                      validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    end = DateTimeLocalField('Activity End',
                    validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    name = StringField('Name',
                       validators=[DataRequired()])
    type = StringField('Type',
                       validators=[DataRequired()])
    kmssact = IntegerField('Activity SS Kms', validators=[Optional()])

    acp = SelectField(u'Activity Cost Profile', coerce=int, validators=[Optional()])
    notes = TextAreaField('Notes')

    submit = SubmitField('Add New Activity')

class UpdateActForm (FlaskForm) :
    start = DateTimeLocalField('Activity Start'
                       , format='%Y-%m-%dT%H:%M')
    end = DateTimeLocalField('Activity End'
                     , format='%Y-%m-%dT%H:%M')
    name = StringField('Name'
                        )
    type = StringField('Type'
                        )
    kmssact = IntegerField('Activity SS Kms', validators=[Optional()])

    acp = SelectField(u'Activity Cost Profile', coerce=int, validators=[Optional()])
    notes = TextAreaField('Notes')

    submit = SubmitField('Update Activity')



