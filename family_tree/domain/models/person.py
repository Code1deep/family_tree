# C:\family_tree\domain\models\person.py
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import or_
from app.extensions import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

class Person(db.Model):
    __tablename__ = 'persons'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=True)
    full_name = db.Column(db.String(100), nullable=False)  
    father_full_name = db.Column(db.String(100), nullable=False)
    friends_name = db.Column(db.String(100))
    image = db.Column(db.String(100))

    mother_id = Column(Integer, ForeignKey('persons.id'))
    father_id = Column(Integer, ForeignKey('persons.id'))
    
    mother = db.relationship('Person', remote_side=[id], foreign_keys=[mother_id], backref='children_from_mother')
    father = db.relationship('Person', remote_side=[id], foreign_keys=[father_id], backref='children_from_father')

    birth_date = db.Column(db.Date)
    death_date = db.Column(db.Date)
    birth_place = db.Column(db.String(200))
    residence = db.Column(db.String(100))
    external_link = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    has_offspring = db.Column(db.Boolean, default=False)
    alive = db.Column(db.Boolean, default=True)
    death_reason = db.Column(db.String(255))
    died_in_battle = db.Column(db.Boolean, default=False)
    known_enemies = db.Column(db.Text)
    fitan = db.Column(db.String(100))
    notes = db.Column(db.Text)
    photo_url = db.Column(db.String(500))
    gender = db.Column(db.String(10), default=True)
    short_bio = db.Column(db.Text)
    full_bio = db.Column(db.Text)
    profession = db.Column(db.String(200))

    __module__ = "domain.models.person"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @property
    def children(self):
        """Tous les enfants (père et mère confondus)"""
        return list(set((self.children_from_father or []) + (self.children_from_mother or [])))

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @full_name.setter
    def full_name(self, value):
        parts = value.strip().split(maxsplit=1)
        self.first_name = parts[0]
        self.last_name = parts[1] if len(parts) > 1 else ""

    @property
    def generation(self):
        """Calcule la génération récursivement"""
        if not self.father and not self.mother:
            return 1
        father_gen = self.father.generation if self.father else 0
        mother_gen = self.mother.generation if self.mother else 0
        return max(father_gen, mother_gen) + 1

    def to_dict(self):
        """Sérialisation pour l'API"""
        return {
            'id': self.id,
            'name': self.full_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'father_full_name': self.father_full_name,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'gender': self.gender,
            'generation': self.generation,
            'father_id': self.father_id,
            'mother_id': self.mother_id,
            'photo_url': self.photo_url
        }
