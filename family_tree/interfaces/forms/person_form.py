# family_tree/interfaces/forms/person_form.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Optional

class PersonForm(FlaskForm):
    # Identité
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    friends_name = StringField('Friends Name', validators=[Optional()])
    fitan = StringField('Fitan', validators=[Optional()])

    # Sexe
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])

    # Dates
    birth_date = DateField('Birth Date', format='%Y-%m-%d', validators=[Optional()])
    death_date = DateField('Death Date', format='%Y-%m-%d', validators=[Optional()])

    # Lieux
    birth_place = StringField('Birth Place', validators=[Optional()])
    residence = StringField('Residence', validators=[Optional()])

    # Famille
    mother_id = IntegerField('Mother ID', validators=[Optional()])
    father_id = IntegerField('Father ID', validators=[Optional()])

    # Biographie
    short_bio = TextAreaField('Short Bio', validators=[Optional()])
    full_bio = TextAreaField('Full Bio', validators=[Optional()])
    profession = StringField('Profession', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])

    # Statut
    has_offspring = BooleanField('Has Offspring')
    alive = BooleanField('Alive')
    death_reason = StringField('Death Reason', validators=[Optional()])
    died_in_battle = BooleanField('Died in Battle')

    # Médias & liens
    external_link = StringField('External Link', validators=[Optional()])
    image_url = StringField('Image URL', validators=[Optional()])
    photo_url = StringField('Photo URL', validators=[Optional()])

    # Autres
    known_enemies = TextAreaField('Known Enemies', validators=[Optional()])
    image = StringField('Image', validators=[Optional()])

