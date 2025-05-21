# C:\family_tree\check_data.py
# (Vérification et visualisation)
from app.factory import create_app
from app.extensions import db
from domain.models.person import Person
from sqlalchemy import or_, and_, not_
import warnings

# Suppress SQLAlchemy 2.0 warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

app = create_app()

def check_circular_references():
    """Vérifie les références circulaires parent-enfant"""
    with app.app_context():
        circular = db.session.query(Person).filter(
            or_(Person.id == Person.father_id, 
                Person.id == Person.mother_id)
        ).count()
        return circular

def check_missing_parents():
    """Vérifie les parents référencés mais inexistants"""
    with app.app_context():
        # Get all existing person IDs once
        existing_ids = {id for (id,) in db.session.query(Person.id).all()}
        
        missing_fathers = db.session.query(Person).filter(
            and_(Person.father_id.isnot(None),
                 not_(Person.father_id.in_(existing_ids)))
        ).count()
        
        missing_mothers = db.session.query(Person).filter(
            and_(Person.mother_id.isnot(None),
                 not_(Person.mother_id.in_(existing_ids)))
        ).count()
        
        return missing_fathers, missing_mothers

def verify_tree_consistency():
    """Effectue toutes les vérifications"""
    with app.app_context():
        print("\n=== VÉRIFICATION DE COHÉRENCE ===")
        
        circular = check_circular_references()
        missing_fathers, missing_mothers = check_missing_parents()
        
        print(f"Relations circulaires: {'❌' if circular else '✅'} {circular} trouvée(s)")
        print(f"Parents pères manquants: {'❌' if missing_fathers else '✅'} {missing_fathers}")
        print(f"Parents mères manquants: {'❌' if missing_mothers else '✅'} {missing_mothers}")

def print_ascii_tree(root_id=None, level=0, max_level=5):
    """Affiche l'arbre en ASCII avec optimisation des requêtes"""
    with app.app_context():
        if root_id is None:
            root = db.session.query(Person).filter_by(father_id=None).first()
            if not root:
                print("Aucune racine trouvée")
                return
            root_id = root.id
        
        # Fetch person and children in one query
        person = db.session.get(Person, root_id)
        if not person:
            return
            
        children = db.session.query(Person).filter(
            or_(Person.father_id == root_id, 
                Person.mother_id == root_id)
        ).order_by(Person.birth_date).all()
        
        prefix = "    " * level
        print(f"{prefix}└── {person.first_name} {person.last_name} (ID:{person.id})")
        
        if level >= max_level:
            print(f"{prefix}    [...] (limite de profondeur {max_level})")
            return
            
        for child in children:
            print_ascii_tree(child.id, level+1, max_level)

def export_family_tree(filename="family_tree.json"):
    """Export optimisé avec une seule requête principale"""
    with app.app_context():
        # Fetch all data in optimized way
        persons = db.session.query(
            Person.id,
            Person.first_name,
            Person.last_name,
            Person.gender,
            Person.father_id,
            Person.mother_id,
            Person.birth_date,
            Person.death_date
        ).all()
        
        # Build ID map
        id_map = {p.id: p for p in persons}
        
        # Prepare data
        data = []
        for p in persons:
            children = [
                c.id for c in persons 
                if c.father_id == p.id or c.mother_id == p.id
            ]
            
            data.append({
                'id': p.id,
                'name': f"{p.first_name} {p.last_name}",
                'gender': p.gender,
                'father_id': p.father_id,
                'mother_id': p.mother_id,
                'birth_date': str(p.birth_date) if p.birth_date else None,
                'death_date': str(p.death_date) if p.death_date else None,
                'children': children
            })
        
        # Save to file
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"Export réussi vers {filename}")

def main_menu():
    """Menu interactif optimisé"""
    while True:
        print("\nOptions:")
        print("1. Vérifier la cohérence de l'arbre")
        print("2. Afficher l'arbre ASCII (5 niveaux max)")
        print("3. Exporter l'arbre (JSON)")
        print("4. Quitter")
        
        choice = input("Votre choix [1-4]: ").strip()
        
        if choice == "1":
            verify_tree_consistency()
        elif choice == "2":
            print("\nARBRE GÉNÉALOGIQUE:")
            print_ascii_tree(max_level=5)
        elif choice == "3":
            export_family_tree()
        elif choice == "4":
            break
        else:
            print("Option invalide. Veuillez choisir 1-4.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    main_menu()