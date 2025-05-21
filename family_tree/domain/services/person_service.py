# domain/services/person_service.py

from typing import Optional
from infrastructure.persistence.repositories.person_repo import PersonRepository
from setup_path import setup_sys_path
setup_sys_path(__file__)

from app.extensions import db
from domain.models.person import Person

class PersonService:
    def __init__(self, repo: Optional[PersonRepository] = None):
        self.repo = repo or PersonRepository()

    def get_by_id(self, person_id: int) -> Optional[Person]:
        return self.repo.get_by_id(person_id)
    
    def get_children(self, person_id):
        """
        Renvoie les enfants (objets Person) pour un parent donné.
        Utilisée par TreeService pour générer l'arbre.
        """
        return self.repo.get_children(person_id)

    def get_person_by_id(self, person_id):
        return self.repo.get(person_id)

    def get_all_persons(self, gender=None):
        return self.repo.get_all(gender=gender)

    def create_person(self, first_name, last_name, gender, birth_date=None, death_date=None, mother_id=None, father_id=None):
        if not first_name or not last_name:
            raise ValueError("First name and last name are required")

        person = Person(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            gender=gender,
            death_date=death_date,
            mother_id=mother_id,
            father_id=father_id
        )
        db.session.add(person)
        db.session.commit()
        return person

    def get_person(self, person_id):
        return self.repo.get(person_id)

    def get_children_details(self, person_id):
        children = self.repo.get_children(person_id)
        return [{
            'id': child.id,
            'first_name': child.first_name,
            'last_name': child.last_name,
            'photo_url': child.photo_url,
            'short_bio': child.short_bio
        } for child in children]
    
    def update_person(self, person_id, updated_data):
        person = self.repo.update(person_id, updated_data)
        if person is None:
            return None
        return person if isinstance(person, dict) else person.to_dict()

    def delete_person(self, person_id: int):
        person = self.repo.get(person_id)
        if not person:
            return False
        self.repo.delete(person)
        self.repo.commit()
        return True

    def get_parents(self, person):
        parents = []
        if person.mother:
            parents.append(person.mother)
        if person.father:
            parents.append(person.father)
        return parents

    def get_person_with_relatives(self, person_id):
        person = self.repo.get_by_id(person_id)
        if not person:
            return None

        def serialize(p):
            if not p:
                return None
            data = {
                'id': p.id,
                'first_name': p.first_name,
                'last_name': p.last_name,
                'photo_url': p.photo_url,
                'short_bio': p.short_bio,
                'children': [],
                'siblings': [],
                'spouses': [],
                'uncles': []
            }
            if p.father_id:
                father = self.repo.get_by_id(p.father_id)
                if father:
                    data['father'] = {
                        'id': father.id,
                        'first_name': father.first_name,
                        'last_name': father.last_name
                    }
            if p.mother_id:
                mother = self.repo.get_by_id(p.mother_id)
                if mother:
                    data['mother'] = {
                        'id': mother.id,
                        'first_name': mother.first_name,
                        'last_name': mother.last_name
                    }
            children = self.repo.get_children(p.id)
            for child in children:
                data['children'].append(serialize(child))

            return data

        return serialize(person)

    def get_all_persons_for_tree(self):
        persons = self.repo.get_all_persons()
        return [{
            "id": p.id,
            "name": p.full_name,
            "gender": p.gender,
            "fid": p.father_id,
            "mid": p.mother_id,
            "pids": p.partner_ids,
            "img": p.photo_url
        } for p in persons]

    def get_basic(self, person_id):
        person = self.repo.get(person_id)
        if not person:
            return {'error': f'Person with id {person_id} not found'}

        return {
            'id': person.id,
            'name': f"{person.first_name} {person.last_name}",
            'gender': person.gender,
            'birth_date': person.birth_date.isoformat() if person.birth_date else None,
            'death_date': person.death_date.isoformat() if person.death_date else None
        }
