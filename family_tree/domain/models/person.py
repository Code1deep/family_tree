# C:\family_tree\domain\models\person.py
from datetime import datetime
from typing import List, Optional, Dict, Any

from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, Boolean, Text, or_
)
from sqlalchemy.orm import relationship, validates

from family_tree.app.extensions import db


class Person(db.Model):
    __tablename__ = 'persons'
    __table_args__ = {'extend_existing': True}

    # Identifiers
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Names
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    friends_name = Column(String(100))
    fitan = Column(String(100))

    # Family relationships
    mother_id = Column(Integer, ForeignKey('persons.id'))
    father_id = Column(Integer, ForeignKey('persons.id'))

    mother = relationship(
        'Person',
        remote_side=[id],
        foreign_keys=[mother_id],
        back_populates='children_from_mother'
    )
    father = relationship(
        'Person',
        remote_side=[id],
        foreign_keys=[father_id],
        back_populates='children_from_father'
    )

    children_from_mother = relationship(
        'Person',
        back_populates='mother',
        foreign_keys=[mother_id],
        lazy='select'
    )
    children_from_father = relationship(
        'Person',
        back_populates='father',
        foreign_keys=[father_id],
        lazy='select'
    )

    # Vital dates
    birth_date = Column(Date)
    death_date = Column(Date)

    # Location
    birth_place = Column(String(200))
    residence = Column(String(100))

    # Biography
    short_bio = Column(Text)
    full_bio = Column(Text)
    profession = Column(String(200))
    notes = Column(Text)

    # Status
    has_offspring = Column(Boolean, default=False)
    alive = Column(Boolean, default=True)
    death_reason = Column(String(255))
    died_in_battle = Column(Boolean, default=False)

    # Media & links
    external_link = Column(String(255))
    image_url = Column(String(255))
    photo_url = Column(String(500))

    # Characteristics
    gender = Column(String(10))
    known_enemies = Column(Text)
    image = Column(String(100))

    __module__ = "domain.models.person"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._normalize_names()

    @validates('first_name', 'last_name')
    def _validate_names(self, key, name):
        if not name or not name.strip():
            raise ValueError(f"{key} cannot be empty")
        return name.strip()

    @property
    def children(self) -> List['Person']:
        """Retourne tous les enfants distincts (union des deux relations)"""
        combined = (self.children_from_father or []) + (self.children_from_mother or [])
        return list({child.id: child for child in combined if child and child.id is not None}.values())

    def to_dict(self) -> Dict[str, Any]:
        if self.birth_date is not None:
            birth_str = self.birth_date.isoformat()
        else:
            birth_str = None

        if self.death_date is not None:
            death_str = self.death_date.isoformat()
        else:
            death_str = None

        return {
            'birth_date': birth_str,
            'death_date': death_str,
            'id': self.id,
            'name': self.full_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'gender': self.gender,
            'generation': self.generation,
            'father_id': self.father_id,
            'mother_id': self.mother_id,
            'photo_url': self.photo_url,
            'is_alive': self.alive,
            'profession': self.profession
        }

    def _normalize_names(self):
        """Normalise les noms lors de l'initialisation"""
        if isinstance(self.first_name, str):
            self.first_name = self.first_name.strip()

        if isinstance(self.last_name, str):
            self.last_name = self.last_name.strip()

    def __repr__(self) -> str:
        return f"<Person {self.id}: {self.full_name}>"

    @property
    def fullname(self) -> str:
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @full_name.setter
    def full_name(self, value: str):
        parts = value.strip().split(maxsplit=1)
        self.first_name = parts[0]
        self.last_name = parts[1] if len(parts) > 1 else ""

    @property
    def generation(self) -> int:
        if not self.father and not self.mother:
            return 1
        father_gen = self.father.generation if self.father else 0
        mother_gen = self.mother.generation if self.mother else 0
        return max(father_gen, mother_gen) + 1
