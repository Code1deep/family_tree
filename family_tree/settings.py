import os

# Chemin de base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuration des fichiers statiques
STATIC_URL = '/static/'  # URL pour les requêtes statiques
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Pour collectstatic
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'family_tree/static'),  # Dossier local
]

# En production sur Render, ajoutez :
if 'RENDER' in os.environ:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
