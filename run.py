# C:\family_tree\run.py
from family_tree.app.factory import create_app
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", default="dev", choices=["dev", "test", "prod"])
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    config_map = {
        "dev": "app.config.DevelopmentConfig",
        "test": "app.config.TestingConfig",
        "prod": "app.config.Config"
    }

    app = create_app(config_map[args.env])
    app.run(debug=args.debug, port=5000)

if __name__ == "__main__":
    main()
