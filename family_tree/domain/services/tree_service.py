# domain/services/tree_service.py

from family_tree.domain.models.person import Person

class TreeService:
    """Service pour les opérations sur l'arbre généalogique"""
    def __init__(self, person_service):
        self.person_service = person_service

    def generate_tree(self, person_id):
        person = self.person_service.get_by_id(person_id)
        if not person:
            return {'nodes': [], 'edges': []}

        nodes = []
        edges = []

        # Ajout de la personne principale
        person_node = {
            'id': person.id,
            'name': f"{person.first_name or ''} {person.last_name or ''}".strip(),
            'photo': person.photo_url,
            'gender': person.gender,
            'data': {
                'mother': self._get_name_by_id(person.mother_id),
                'bio': f"Né(e) en {person.birth_date}, {person.birth_place or ''}"
            }
        }
        if getattr(person, "partner_ids", None):
            person_node["pids"] = person.partner_ids
        nodes.append(person_node)

        # Ajout des parents
        for parent_role in ['mother_id', 'father_id']:
            parent_id = getattr(person, parent_role)
            if parent_id:
                parent = self.person_service.get_by_id(parent_id)
                if parent:
                    parent_node = {
                        'id': parent.id,
                        'name': f"{parent.first_name or ''} {parent.last_name or ''}".strip(),
                        'photo': parent.photo_url,
                        'gender': parent.gender,
                        'data': {
                            'mother': self._get_name_by_id(parent.mother_id),
                            'bio': f"Né(e) en {parent.birth_date}, {parent.birth_place or ''}"
                     }
                    }
                    nodes.append(parent_node)
                    edges.append({'from': parent.id, 'to': person.id})

        # Ajout des enfants
        children = self.person_service.get_children(person.id)
        for child in children:
            child_node = {
                'id': child.id,
                'name': f"{child.first_name or ''} {child.last_name or ''}".strip(),
                'photo': child.photo_url,
                'gender': child.gender,
                'data': {
                    'mother': self._get_name_by_id(child.mother_id),
                    'bio': f"Né(e) en {child.birth_date}, {child.birth_place or ''}"
                }
            }
            nodes.append(child_node)
            edges.append({'from': person.id, 'to': child.id})

        return {
            'nodes': nodes,
            'edges': edges
        }

    def _get_name_by_id(self, person_id): 
        """Renvoie le nom complet d'une personne via son ID"""
        if not person_id:
            return ""
        person = self.person_service.get_by_id(person_id)
        return person.fullname if person else ""
   
    def get_all_persons(self):
        """Récupère toutes les personnes"""
        return Person.query.all()
    
    def find_root_ancestor(self, person_id=None):
        """Trouve l'ancêtre racine de l'arbre"""
        if person_id:
            person = Person.query.get(person_id)
            if person:
                return self._find_oldest_ancestor(person)
        return self._find_oldest_in_db()
    
    def _find_oldest_ancestor(self, person):
        """Trouve récursivement l'ancêtre le plus ancien"""
        if person.father:
            return self._find_oldest_ancestor(person.father)
        if person.mother_rel:
            return self._find_oldest_ancestor(person.mother_rel)
        return person
    
    def _find_oldest_in_db(self):
        """Trouve la personne sans parents dans la DB"""
        roots = Person.query.filter(
            (Person.father_id.is_(None)) & 
            (Person.mother_id.is_(None))
        ).all()
        return roots[0] if roots else None
    
    def calculate_generation(self, person):
        """Calcule la génération d'une personne"""
        return person.generation
    
    def get_family_branch(self, person_id, depth=3):
        """Récupère une branche familiale avec une profondeur donnée"""
        person = Person.query.get(person_id)
        if not person:
            return None
            
        return self._build_branch(person, depth)
    
    def _build_branch(self, person, depth):
        """Construit récursivement une branche de l'arbre"""
        if depth == 0:
            return None
            
        branch = {
            'person': person.to_dict(),
            'children': []
        }
        
        for child in person.children:
            child_branch = self._build_branch(child, depth-1)
            if child_branch:
                branch['children'].append(child_branch)
                
        return branch
