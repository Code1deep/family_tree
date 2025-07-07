# interfaces/api/resources/person/routes_api.py

from venv import logger
from flask import render_template, request, jsonify, abort
from interfaces.api.serializers.person_serializer import PersonSerializer
from domain.models import Person
from app.extensions import db
from infrastructure.persistence.repositories import PersonRepository

person_service = None
repo = PersonRepository()

def inject_service(service):
    global person_service
    person_service = service

def register_api_routes(person_api):

    @person_api.route('/person/<int:person_id>')
    def person_profile(person_id):
        person = repo.get_person_with_relatives(person_id)
        if not person:
            abort(404)

        # Parents
        father_name = person.father.full_name if person.father and person.father.full_name else "غير معروف"
        mother_name = person.mother.first_name if person.mother else "غير معروفة"

        # Enfants
        children = []
        if person.children_from_father:
            children.extend(person.children_from_father)
        if person.children_from_mother:
            children.extend(person.children_from_mother)

        # Frères/soeurs : autres enfants des mêmes parents
        siblings = []
        if person.father:
            siblings.extend([
                c for c in person.father.children_from_father if c.id != person.id
            ])
        if person.mother:
            siblings.extend([
                c for c in person.mother.children_from_mother if c.id != person.id
            ])

        # Oncles/tantes : frères/soeurs du père et de la mère
        uncles = []
        aunts = []

        # Frères/soeurs du père
        if person.father and person.father.father_id:
            paternal_grandfather = repo.get(person.father.father_id)
            if paternal_grandfather:
                for uncle in repo.get_children(paternal_grandfather.id):
                    if uncle.id != person.father.id:
                        if uncle.gender == "M":
                            uncles.append(uncle)
                        else:
                            aunts.append(uncle)

        # Frères/soeurs de la mère
        if person.mother and person.mother.father_id:
            maternal_grandfather = repo.get(person.mother.father_id)
            if maternal_grandfather:
                for uncle in repo.get_children(maternal_grandfather.id):
                    if uncle.id != person.mother.id:
                        if uncle.gender == "M":
                            uncles.append(uncle)
                        else:
                            aunts.append(uncle)

        return render_template(
            'person_bio.html',
            person={
                "id": person.id,
                "name": f"{person.first_name} {person.last_name}",
                "father_id": person.father_id,
                "mother_id": person.mother_id,
                "father_name": father_name,
                "mother_name": mother_name,
                "birth_date": person.birth_date,
                "death_date": person.death_date,
                "death_reason": person.death_reason,
                "birth_place": person.birth_place,
                "residence": person.residence,
                "short_bio": person.short_bio
            },
            children=children,
            siblings=siblings,
            uncles=uncles,
            aunts=aunts
        )

    @person_api.route('/person/<int:person_id>/details')
    def person_details(person_id):
        person = repo.get_person_with_relatives(person_id)
        if not person:
            abort(404)

        # Nom complet
        name = f"{person.first_name} {person.last_name}"

        # Timeline (EXEMPLE : à adapter)
        timeline = []
        if person.birth_date:
            timeline.append({
                "date": person.birth_date.strftime("%Y-%m-%d"),
                "description": "تاريخ الميلاد"
            })
        if person.death_date:
            timeline.append({
                "date": person.death_date.strftime("%Y-%m-%d"),
                "description": "تاريخ الوفاة"
            })

        # Parents
        parents = []
        if person.father:
            parents.append({
                "id": person.father.id,
                "name": person.father.full_name or f"{person.father.first_name} {person.father.last_name}"
            })
        if person.mother:
            parents.append({
                "id": person.mother.id,
                "name": f"{person.mother.first_name} {person.mother.last_name}"
            })

        # Siblings
        siblings = []
        if person.father:
            siblings.extend([
                {"id": s.id, "name": f"{s.first_name} {s.last_name}"}
                for s in person.father.children_from_father if s.id != person.id
            ])
        if person.mother:
            siblings.extend([
                {"id": s.id, "name": f"{s.first_name} {s.last_name}"}
                for s in person.mother.children_from_mother if s.id != person.id
            ])

        # Spouses (EXEMPLE : il faut avoir un champ ou une table)
        spouses = []  # Remplis cette liste si tu gères les mariages

        # Achievements & gallery (EXEMPLE : à adapter)
        achievements = []
        gallery = []

        return render_template(
            'person_details.html',
            person={
                "id": person.id,
                "name": name,
                "image": None,  # ou person.photo_url si tu as
                "bio_full": person.full_bio or person.short_bio,
                "timeline": timeline,
                "parents": parents,
                "siblings": siblings,
                "spouses": spouses,
                "achievements": achievements,
                "gallery": gallery
            }
        )


    @person_api.route('/api/person/<int:person_id>')
    def get_person_by_id(person_id):
        logger.info(f"[METHOD] get_person_by_id({person_id})")
        person = person_service.get_by_id(person_id)
        if not person:
            abort(404, "Person not found")
        return jsonify(person)

    @person_api.route('/api/person/<int:person_id>/children')
    def get_person_children(person_id):
        logger.info(f"[METHOD] get_person_children({person_id})")
        children = person_service.get_children(person_id)
        return jsonify([PersonSerializer.serialize_basic(c) for c in children])

    @person_api.route('/api/person')
    def get_person_query():
        person_id = request.args.get('id', type=int)
        if not person_id:
            abort(400, "Missing person id")

        include = request.args.get('include', '')
        try:
            if 'relatives' in include:
                return jsonify(person_service.get_with_relatives(person_id))
            return jsonify(person_service.get_basic(person_id))
        except ValueError as e:
            abort(404, str(e))

    @person_api.route('/api/persons', methods=['GET'], endpoint='search_persons')
    def search_persons():
        name = request.args.get('name')
        gender = request.args.get('gender')

        query = Person.query
        if name and name.strip():
            query = query.filter(
                (Person.first_name.ilike(f"%{name}%")) |
                (Person.last_name.ilike(f"%{name}%"))
            )
        if gender:
            query = query.filter(Person.gender.ilike(gender))

        persons = query.all()
        return jsonify([p.to_dict() for p in persons])

