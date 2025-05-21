# C:\family_tree\setup.py
from setuptools import setup, find_packages

setup(
    name="family_tree",
    version="1.0.0",
    description="Application Flask de gestion de généalogie",
    author="Ton Nom",
    packages=find_packages(include=["app*", "interfaces*", "domain*", "infrastructure*"]),
    include_package_data=True,
    install_requires=[
        'flask==2.2.5',
        'flask-sqlalchemy==3.1.1',
        'gunicorn==23.0.0',
        'flask-login==0.6.3',
        'flask-babel==2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'run-family-tree = run:main'
        ]
    },
    python_requires=">=3.8",
)

