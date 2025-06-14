# infrastructure/visualization/tree_visualizer.py
from platform import node
from typing import Optional
from family_tree.app.factory import db
from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository 

from family_tree.domain.services.person_service import PersonService
from flask import current_app, url_for
from interfaces.api.serializers.person_serializer import PersonSerializer
from family_tree.domain.models.person import Person
from family_tree.domain.services.tree_service import TreeService 

def get_visualizer():
    return FamilyTreeVisualizer(current_app, PersonRepository(db.session))

class FamilyTreeVisualizer:
    def __init__(self, app, person_repo: PersonRepository):
        self.app = app
        self.person_repo = person_repo

    def generate_familytree_data(self, root_person_id: Optional[int] = None):
        try:
            if root_person_id is None:
                root_person_id = 1  # Valeur par défaut pour éviter plantage

            person = self.person_repo.get_person_with_relatives(root_person_id)
            if not person:
                return {"nodes": [], "edges": []}

            nodes = self._generate_nodes(person, visited_nodes=set())
            edges = self._generate_edges(person, visited_edges=set())

            return {
                "nodes": nodes,
                "edges": edges
            }
        except Exception as e:
            current_app.logger.exception(f"Error generating tree: {e}")
            raise

    def _generate_nodes(self, person, visited_nodes: set):
        nodes = []
        person_id = self._get_person_id(person)
        if person_id in visited_nodes:
            return nodes
        visited_nodes.add(person_id)

        full_name = f"{self._get_attr(person, 'first_name')} {self._get_attr(person, 'last_name')}"
        node = {
            "id": person_id,
            "name": full_name,
            "data": {
                "generation": self._calculate_generation(person),
                "bio": self._get_attr(person, 'short_bio') or '',
                "mother": self._get_parent_name(self._get_attr(person, 'mother')),
                "father": self._get_parent_name(self._get_attr(person, 'father')),
            },
            "photo": self._get_attr(person, 'photo_url'),
        }
        nodes.append(node)

        # Fusionner les enfants issus du père et de la mère
        children_f = self._get_attr(person, 'children_from_father') or []
        children_m = self._get_attr(person, 'children_from_mother') or []
        all_children = {self._get_person_id(c): c for c in children_f + children_m}.values()
        for child in all_children:
            nodes.extend(self._generate_nodes(child, visited_nodes))
        return nodes
    def _generate_edges(self, person, visited_edges: set):
        edges = []
        person_id = self._get_person_id(person)
        if person_id is None:
            return edges
        for parent_type in ['father', 'mother']:
            parent = self._get_attr(person, parent_type)
            if parent:
                parent_id = self._get_person_id(parent)
                if parent_id is None:
                    continue
                edge_key = (parent_id, person_id)
                if edge_key in visited_edges:
                    continue
                visited_edges.add(edge_key)
                edge = {
                    "from": parent_id,
                    "to": person_id,
                    "type": parent_type,
                    "color": "#3498db" if parent_type == "father" else "#e74c3c"
                }
                if parent_type == "mother":
                    edge["dashes"] = True
                edges.append(edge)
        children_f = self._get_attr(person, 'children_from_father') or []
        children_m = self._get_attr(person, 'children_from_mother') or []
        all_children = {self._get_person_id(c): c for c in children_f + children_m}.values()
        for child in all_children:
            edges.extend(self._generate_edges(child, visited_edges))
        return edges
    def _calculate_generation(self, person):
        def helper(p, generation=0):
            father = self._get_attr(p, 'father')
            mother = self._get_attr(p, 'mother')
            if father:
                return helper(father, generation + 1)
            elif mother:
                return helper(mother, generation + 1)
            return generation
        return helper(person)
    def _get_person_id(self, person):
        if person is None:
            return None
        if isinstance(person, dict):
            person_id = person.get('id')
        else:
            person_id = getattr(person, 'id', None)

        if person_id is None:
            return None

        return int(person_id)

    
    def _get_attr(self, person, attr):
        if isinstance(person, dict):
            return person.get(attr, None)
        return getattr(person, attr, None)
    
    def _get_parent_name(self, parent):
        if parent is None:
            return "Inconnue"
        first = self._get_attr(parent, 'first_name') or ''
        last = self._get_attr(parent, 'last_name') or ''
        return f"{first} {last}".strip()

