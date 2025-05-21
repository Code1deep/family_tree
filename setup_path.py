# C:\family_tree\setup_path.py
import sys
from pathlib import Path

def setup_sys_path(current_file: str, target_folder: str = "family_tree"):
    """
    Ajoute dynamiquement le dossier `target_folder` au sys.path,
    en partant du fichier actuel (__file__).
    
    :param current_file: généralement __file__
    :param target_folder: nom du dossier racine de ton projet
    """
    path = Path(current_file).resolve()
    while path.name != target_folder and path.parent != path:
        path = path.parent

    if path.name == target_folder:
        sys.path.insert(0, str(path))
    else:
        raise RuntimeError(f"Impossible de trouver le dossier racine '{target_folder}' à partir de {current_file}")
