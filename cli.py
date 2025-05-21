from app import create_app
from flask_migrate import cli

app = create_app()

if __name__ == '__main__':
    cli.main()