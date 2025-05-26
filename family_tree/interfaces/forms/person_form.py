# family_tree/interfaces/forms/person_form.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, Optional

class PersonForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    birth_date = DateField('Birth Date', format='%Y-%m-%d', validators=[Optional()])
    death_date = DateField('Death Date', format='%Y-%m-%d', validators=[Optional()])
    mother_id = IntegerField('Mother ID', validators=[Optional()])
    father_id = IntegerField('Father ID', validators=[Optional()])
