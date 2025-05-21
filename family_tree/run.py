# C:\family_tree\run.py
from setup_path import setup_sys_path
setup_sys_path(__file__)

import argparse
from app.factory import create_app

def main():
    parser = argparse.ArgumentParser(description="Lancement de l'application Family Tree")
    parser.add_argument("--env", default="dev", choices=["dev", "test", "prod"], help="Profil de configuration")
    parser.add_argument('--debug', action='store_true', help="Activer le mode debug")
    args = parser.parse_args()

    config_map = {
        "dev": "app.config.DevelopmentConfig",
        "test": "app.config.TestingConfig",
        "prod": "app.config.Config"
    }

    app = create_app(config_map[args.env])

    print(f"\n✓ Environnement utilisé : {args.env}")
    print("\n✓ Routes disponibles :")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:30s} ➜ {rule}")

    #app.run(host='0.0.0.0', port=5000, debug=(args.env != "prod"))
    app.run(debug=args.debug, host="127.0.0.1", port=5000)

if __name__ == '__main__':
    main()



