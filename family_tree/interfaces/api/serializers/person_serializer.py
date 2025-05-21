# C:\family_tree\interfaces\api\serializers\person_serializer.py 

from setup_path import setup_sys_path
setup_sys_path(__file__)

from datetime import datetime
from domain.models.person import Person  # Import clair depuis le domaine

class PersonSerializer:
    """Sérialiseur dédié à la conversion des objets Person dans différents formats"""

    @staticmethod
    def serialize(person):
        """
        Version minimale utilisée pour des affichages simples.
        ⚠️ Ne contient pas le champ 'gender' !
        """
        if not person:
            return None

        return {
            'id': person.id,
            'full_name': f"{person.first_name} {person.last_name}",
            'birth_date': person.birth_date.isoformat() if person.birth_date else None
        }

    @staticmethod
    def serialize_for_api(person):
        """
        Version recommandée pour les réponses d'API publiques.
        Contient les informations essentielles : prénom, nom, genre, etc.
        ✅ Inclut 'gender' => à utiliser dans la route GET /persons
        """
        return {
            'id': person.id,
            'full_name': f"{person.first_name} {person.last_name}",  # champ utile pour affichage direct
            'first_name': person.first_name,
            'last_name': person.last_name,
            'gender': person.gender,  # requis pour les filtres et les tests
            'birth_date': person.birth_date.isoformat() if person.birth_date else None,
            'death_date': person.death_date.isoformat() if person.death_date else None,
            # ➕ Tu peux ajouter d'autres champs ici si besoin (ex: 'alive', 'profession', etc.)
        }

    @staticmethod
    def serialize_basic(person):
        """
        Version très simplifiée : uniquement prénom + nom.
        ❌ Pas de 'gender' ni de dates.
        """
        return {
            'id': person.id,
            'full_name': f"{person.first_name} {person.last_name}",
            'first_name': person.first_name,
            'last_name': person.last_name
        }

    @staticmethod
    def serialize_for_export(person):
        """
        Format adapté pour export CSV/Excel.
        Utilise des clés en français + formatage date DD/MM/YYYY.
        """
        if not person:
            return None

        return {
            'ID': person.id,
            'Prénom': person.first_name,
            'Nom': person.last_name,
            'full_name': f"{person.first_name} {person.last_name}",
            'Date de naissance': person.birth_date.strftime('%d/%m/%Y') if person.birth_date else ''
        }
