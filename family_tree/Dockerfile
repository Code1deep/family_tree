# Image officielle Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /opt/render/project/src

# Copier le projet dans le conteneur
COPY . .

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exposer le port (Render le gère mais bon à garder pour clarté)
EXPOSE 8000

# Démarrage : gunicorn sans colon
CMD ["gunicorn", "family_tree.wsgi", "--bind", "0.0.0.0:8000"]
