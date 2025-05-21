# C:\family_tree\main.py
import sys
from pathlib import Path

# Solution ABSOLUE pour les imports
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from app.factory import create_app
    print("✓ Import de create_app RÉUSSI")
except ImportError as e:
    print(f"✗ Erreur d'import : {e}")
    raise

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)