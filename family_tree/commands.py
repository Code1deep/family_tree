# family_tree/commands.py
import click
from flask.cli import with_appcontext
from family_tree.insertion import full_initialize

@click.command("init-data")
@with_appcontext
def init_data():
    full_initialize()
    click.echo("✅ Données insérées !")
