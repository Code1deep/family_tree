# C:\family_tree\wsgi.py

import sys
from pathlib import Path

# Ajout explicite du chemin Render
sys.path.append('/opt/render/project/src')

# Import après avoir configuré le path
from app.factory import create_app

app = create_app()






