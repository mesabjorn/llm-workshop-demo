import click
from flask import current_app
from models.User import db


def init_db(app):
    db.init_app(app)

def create_db(app):
    with app.app_context():
        db.create_all()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    create_db(current_app)
    click.echo('Initialized the database.')

def register_init_db_command(app):
    "allows initializing database with 'flask init-db'"
    app.cli.add_command(init_db_command)
    