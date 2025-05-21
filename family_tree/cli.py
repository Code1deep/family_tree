# C:\family_tree\cli.py
import os
import click
from flask.cli import FlaskGroup
from app.factory import create_app
from populate_data import main as populate_main
from rebuild_db import main as rebuild_main
from inspect_db import main as inspect_main
from check_data import main as check_main

# Sélection de la config via variable d’environnement ou fallback
config_name = os.getenv("FAMILYTREE_ENV", "app.config.DevelopmentConfig")
app = create_app(config_name)

@click.group(cls=FlaskGroup, create_app=lambda: app)
def cli():
    """Interface CLI de l'application Family Tree"""
    pass

@cli.command("runserver")
@click.option("--host", default="127.0.0.1", help="Hôte")
@click.option("--port", default=5000, help="Port")
@click.option("--debug", is_flag=True, help="Activer le mode debug")
def runserver(host, port, debug):
    """Démarre le serveur Flask"""
    app.run(host=host, port=port, debug=debug)

@cli.command("routes")
def show_routes():
    """Affiche les routes disponibles"""
    for rule in app.url_map.iter_rules():
        click.echo(f"{rule.endpoint:30s} ➜ {rule}")

@cli.command("populate")
def populate():
    """Peuple la base de données avec des données d'exemple"""
    populate_main()

@cli.command("rebuild")
def rebuild():
    """Réinitialise la base (drop + recreate)"""
    rebuild_main()

@cli.command("inspect")
def inspect():
    """Inspecte la base de données"""
    inspect_main()

@cli.command("check")
def check():
    """Vérifie la validité des données"""
    check_main()

if __name__ == "__main__":
    cli()
