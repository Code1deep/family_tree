# Base image Python légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /opt/render/project/src/family_tree

# Copier tout le projet dans le conteneur
COPY . .

# Mettre à jour pip et installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exposer le port (optionnel car Render gère ça automatiquement)
EXPOSE 8000

# Créer un script de démarrage sans ":" dans la commande
RUN echo 'from gunicorn.app.wsgiapp import run\nif __name__ == "__main__":\n    run()' > start_server.py

# Commande de démarrage : pas de ":"
CMD ["python", "start_server.py", "family_tree.wsgi"]
