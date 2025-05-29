# infrastructure/persistence/repositories/person_repo.py

from family_tree.domain.models.person import Person
from family_tree.app.extensions import db
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from family_tree.domain.services.tree_service import TreeService
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class PersonRepository:
    def __init__(self, session: Session = db.session): 
        self.session = session

    def delete(self, person):
        self.session.delete(person)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def get(self, person_id):
        print(f">>> DEBUG: appel à get({person_id}) dans PersonRepository")
        return self.session.get(Person, person_id)

    def get_all(self):
        return self.session.query(Person).all()

    def get_person_with_relatives(self, person_id):
        if not person_id or person_id <= 0:
            return None

        try:
            person = (
                self.session.query(Person)
                .options(
                    joinedload(Person.father),
                    joinedload(Person.mother),
                    joinedload(Person.children_from_father),
                    joinedload(Person.children_from_mother)
                )
                .filter(Person.id == person_id)
                .first()
            )
            return person
        except Exception as e:
            logger.error(f"Error loading person with relatives: {str(e)}")
            return None

    # Compatibilité avec anciens appels
    def get_by_id(self, person_id: int):
        return self.session.query(Person).filter(Person.id == person_id).first()

    def get_person_by_id(self, person_id):
        return self.get(person_id)

    def get_all_persons(self):
        return self.get_all()

    def get_children(self, parent_id):
        """
        Renvoie les enfants pour un parent donné.
        parent_id peut être un entier ou un tuple/list contenant un entier.
        """
        try:
            # Si parent_id est un tuple ou une liste, en extraire le premier élément
            if isinstance(parent_id, (list, tuple)):
                parent_id = parent_id[0]
            else:
                # Forcer la conversion au cas où
                parent_id = int(parent_id)
        except Exception as e:
            raise ValueError(f"parent_id doit être convertible en entier, obtenu : {parent_id}")

        return self.session.query(Person).filter(
            (Person.father_id == parent_id) | (Person.mother_id == parent_id)
        ).all()

    def get_parents(self, person):
        parents = []
        if person.father_id:
            father = self.session.get(Person, person.father_id)
            if father:
                parents.append(father)
        if person.mother_id:
            mother = self.session.get(Person, person.mother_id)
            if mother:
                parents.append(mother)
        return parents

    def add_person(self, data_or_person):
        if isinstance(data_or_person, Person):
            person = data_or_person
        else:
            person = Person(
                first_name=data_or_person.get("first_name"),
                last_name=data_or_person.get("last_name"),
                gender=data_or_person.get("gender"),
                birth_date=data_or_person.get("birth_date"),
                death_date=data_or_person.get("death_date"),
                father_id=data_or_person.get("father_id"),
                mother_id=data_or_person.get("mother_id")
            )
        self.session.add(person)
        self.session.commit()
        return person

    def generate_tree_data(self, person_id: int) -> Dict:
        tree_service = TreeService(self)
        try:
            raw_data = tree_service.generate_tree(person_id)
            if not raw_data or not isinstance(raw_data, dict):
                return {'nodes': [], 'edges': []}

            nodes = []
            for node in raw_data.get('nodes', []):
                formatted_node = {
                    'id': node.get('id'),
                    'pids': node.get('partner_ids', []),
                    'img': node.get('photo_url'),
                    'name': f"{node.get('first_name', '')} {node.get('last_name', '')}".strip()
                }

                nodes.append(formatted_node)

            return {
                'nodes': nodes,
                'edges': raw_data.get('edges', [])
            }

        except Exception as e:
            logger.error(f"Error generating tree: {str(e)}")
            return {'nodes': [], 'edges': []}

    def get_by_name(self, name):
        return self.session.query(Person)\
            .filter(
                (Person.first_name + " " + Person.last_name).ilike(f'%{name}%') |
                Person.first_name.ilike(f'%{name}%') |
                Person.last_name.ilike(f'%{name}%')
            )\
            .all()

    def update(self, person_id, updated_data):
        person = self.get(person_id)
        if not person:
            return None

        for key, value in updated_data.items():
            if hasattr(person, key):
                setattr(person, key, value)

        self.session.commit()
        return person

    def get_all(self, gender=None):
        query = self.session.query(Person)
        if gender:
            query = query.filter(Person.gender.ilike(gender))  # insensible à la casse
        return query.all()
