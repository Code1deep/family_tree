# family_tree/bootstrap.py
import sys
from pathlib import Path

def setup_paths():
    root = Path(__file__).parent.resolve()
    sys.path.insert(0, str(root))
    
    # Vérification
    print(f"✓ Chemins configurés : {sys.path[0]}")