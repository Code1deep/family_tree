# C:\family_tree\wsgi.py
import sys
from pathlib import Path

# Configuration explicite des chemins pour Render
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))  # Chemin principal du projet
sys.path.append('/opt/render/project/src')  # Chemin spécifique à Render

# Debug - Affiche les chemins Python
print("\n=== PYTHON PATHS ===")
for path in sys.path:
    print(path)
print("===================\n")

# Import de l'application après configuration des chemins
try:
    from family_tree.app.factory import create_app
    print("✓ Import de create_app réussi")
except ImportError as e:
    print(f"❌ Erreur d'import : {e}")
    raise

# Création de l'application
app = create_app()

# Point d'entrée pour l'exécution locale
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)






