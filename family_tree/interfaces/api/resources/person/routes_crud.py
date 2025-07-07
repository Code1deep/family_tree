# interfaces/api/resources/person/routes_crud.py
import logging
from datetime import datetime
from typing import Optional
from flask import render_template, request, jsonify, abort, redirect, url_for, flash
from app.extensions import db
from interfaces.api.serializers.person_serializer import PersonSerializer
from flask import render_template, abort
from domain.models.person import Person

person_service = None

def inject_service(service):
    global person_service
    person_service = service

def calculate_generation_id(birth_date: str, father_id: Optional[int]) -> str:
    birth_year = int(birth_date.split("-")[0]) if birth_date else None

    generation_num = 1
    if father_id:
        father = Person.query.get(father_id)
        if father and father.birth_date:
            father_year = int(father.birth_date.split("-")[0])
            if father_year and birth_year:
                diff = birth_year - father_year
                if diff > 20:
                    generation_num = father.generation + 1
                else:
                    generation_num = father.generation
            else:
                generation_num = father.generation
        else:
            generation_num = 1
    return f"{birth_year}_G{generation_num}_{father_id or 'NA'}"

def register_crud_routes(person_api):
    @person_api.route('/crud/person/<int:person_id>', methods=['DELETE'])
    def delete_person(person_id):
        if person_service.delete(person_id):
            return jsonify({'success': True}), 204
        abort(404, "Person not found")

    @person_api.route('/persons', methods=['POST'])
    def create_person():
        """Endpoint POST /persons - Création personne"""
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        try:
            # Vérification explicite des champs obligatoires
            required_fields = ['first_name', 'last_name', 'full_name', 'gender']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f"Missing required field: {field}"}), 400

            # 🔁 Conversion des dates
            def parse_date(field):
                value = data.get(field)
                if value:
                    try:
                        return datetime.strptime(value, "%Y-%m-%d").date()
                    except ValueError:
                        return jsonify({'error': f"Invalid date format for {field}, expected YYYY-MM-DD"}), 400
                return None

            birth_date = parse_date('birth_date')
            if isinstance(birth_date, tuple): return birth_date  # early return if error
            death_date = parse_date('death_date')
            if isinstance(death_date, tuple): return death_date

            # Création manuelle avec full_name saisi
            person = person_service.create_person(
                first_name=data['first_name'].strip(),
                last_name=data['last_name'].strip(),
                full_name=data['full_name'].strip(),
                father_full_name=data['father_full_name'].strip(),
                gender=data['gender'],
                birth_date=birth_date,
                death_date=death_date,
                mother_id=data.get('mother_id'),
                father_id=data.get('father_id')
            )
            return jsonify(person.to_dict()), 201

        except Exception as e:
            logging.error(f"Error creating person: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500


    @person_api.route('/persons/<int:person_id>', methods=['GET'])
    def get_person(person_id):
        """Récupérer une personne par ID via /persons"""
        person = person_service.get_person_by_id(person_id)
        if not person:
            return jsonify({'error': 'Person not found'}), 404
        return jsonify(person.to_dict()), 200

    @person_api.route('/persons', methods=['GET'])
    def list_persons():
        """Lister toutes les personnes"""
        persons = person_service.get_all_persons()
        return jsonify([PersonSerializer.serialize_for_api(p) for p in persons])
    
    @person_api.route('/persons/<int:person_id>', methods=['PUT'])
    def update_person_by_service(person_id):
        """Met à jour une personne via /persons/<id>"""
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        try:
            person = person_service.get_person_by_id(person_id)
            if not person:
                return jsonify({'error': 'Person not found'}), 404

            for field in ['first_name', 'last_name', 'full_name','gender', 'birth_date', 'death_date', 'mother_id', 'father_id']:
                if field in data:
                    setattr(person, field, data[field])

            db.session.commit()
            return jsonify(person.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating person: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @person_api.route('/persons/<int:person_id>', methods=['DELETE'])
    def delete_person_by_service(person_id):
        """Supprimer une personne via /persons/<id>"""
        try:
            success = person_service.delete_person(person_id)
            if not success:
                return jsonify({'error': 'Person not found'}), 404
            return '', 204
        except Exception as e:
            person_service.repo.rollback()  
            logging.error(f"Error deleting person: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
        
    #from flask import render_template_string
    from interfaces.forms.person_form import PersonForm

    from flask import Blueprint, request, render_template, render_template_string, redirect, url_for, flash

    @person_api.route('/add', methods=['GET', 'POST'])
    def add_person():
        print("✅ ROUTE ADD_PERSON APPELÉE")
        from interfaces.forms.person_form import PersonForm
        form = PersonForm()
        all_persons = Person.query.all()
        print("🔍 ATTRS DU FORM :", dir(form))
        print("✔ father_full_name présent :", hasattr(form, "father_full_name"))

        print("📌 Nouvelle requête /add method =", request.method)
        print("📌 form data:", request.form)
        print("📌 files:", request.files)
        print("📌 validate_on_submit:", form.validate_on_submit())

        if form.validate_on_submit():
            print("✅ ON PASSE ICI validate_on_submit()")
            try:
                mother_id = form.mother_id.data.id if form.mother_id.data else None
                father_id = form.father_id.data.id if form.father_id.data else None
                print("📌 mother_id:", mother_id)
                print("📌 father_id:", father_id)
                # Après avoir extrait birth_date et father_id
                birth_date = form.birth_date.data.isoformat() if form.birth_date.data else None

                new_person = Person(
                    first_name=form.first_name.data.strip(),
                    last_name=form.last_name.data.strip(),
                    full_name=form.full_name.data.strip(),
                    father_full_name=form.father_full_name.data.strip(),
                    friends_name=form.friends_name.data,
                    gender=form.gender.data,
                    birth_date=form.birth_date.data.isoformat() if form.birth_date.data else None,
                    death_date=form.death_date.data.isoformat() if form.death_date.data else None,
                    birth_place=form.birth_place.data,
                    residence=form.residence.data,
                    mother_id=mother_id if mother_id else None,
                    father_id=father_id if father_id else None,
                    short_bio=form.short_bio.data,
                    profession=form.profession.data,
                    notes=form.notes.data,
                    has_offspring=form.has_offspring.data,
                    alive=form.alive.data,
                    death_reason=form.death_reason.data,
                    died_in_battle=form.died_in_battle.data,
                    external_link=form.external_link.data,
                    image_url=form.image_url.data,
                    photo_url=form.photo_url.data,
                    known_enemies=form.known_enemies.data,
                    image=form.image.data
                )

                # Calcul de generation_id
                new_person.generation_id = calculate_generation_id(birth_date, father_id)
                
                db.session.add(new_person)
                db.session.commit()
                print("✅ Person added OK id =", new_person.id)
                flash("✅ شخص جديد أضيف بنجاح", "success")
                return redirect(url_for('person_api.add_person'))

            except Exception as e:
                print("❌ ERREUR LORS DE L'INSERTION :", repr(e))
                db.session.rollback()
                return f"Erreur serveur: {repr(e)}", 500

        print("📌 Form non validé → retourne le formulaire")
        return render_template('form.html', form=form, all_persons=all_persons,
                            males=[p for p in all_persons if p.gender == 'male'],
                            females=[p for p in all_persons if p.gender == 'female'])


    @person_api.route('/new_person_form', methods=['GET'])
    def new_person_form():
        from interfaces.forms.person_form import PersonForm
        form = PersonForm()
        return render_template('tree_form.html', form=form)

