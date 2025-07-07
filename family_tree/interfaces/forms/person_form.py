# family_tree/interfaces/forms/person_form.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from domain.models.person import Person

class PersonForm(FlaskForm):
    # Identité
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired()]) 
    father_full_name = StringField('Father Full Name', validators=[DataRequired()]) 
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
    father_id = QuerySelectField(
        'Father',
        query_factory=lambda: Person.query.filter_by(gender='male').all(),
        get_label=lambda p: p.full_name,
        allow_blank=True
    )

    mother_id = QuerySelectField(
        'Mother',
        query_factory=lambda: Person.query.filter_by(gender='female').all(),
        get_label=lambda p: p.full_name,
        allow_blank=True
    )

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
