from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Required

class Intro(Form):
    user = StringField('Enter your Twitter handle:', validators=[DataRequired()])
    submit = SubmitField('Find my lists')

class ListDrop(Form):
    which = SelectField('Which list?', coerce=int)
    hours = StringField('How many hours?')
    submit = SubmitField('Rank \'em!')
