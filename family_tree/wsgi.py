# C:\family_tree\wsgi.py
#from setup_path import setup_sys_path
#setup_sys_path(__file__)
import sys
from pathlib import Path

# Ajout explicite du chemin Render
sys.path.append('/opt/render/project/src')

# Import après avoir configuré le path
from app.factory import create_app

app = create_app()






