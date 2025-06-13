# Base image officielle Python
FROM python:3.11-slim

# Empêche Python de bufferiser les logs (utile pour Render logs en temps réel)
ENV PYTHONUNBUFFERED=1

# Crée un répertoire de travail
WORKDIR /opt/render/project/src/family_tree

# Copie les fichiers nécessaires
COPY . .

# Met à jour pip et installe les dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose le port (Render n'en a pas besoin explicitement mais utile si tu testes en local)
EXPOSE 8000

# Commande de démarrage
CMD gunicorn family_tree.wsgi:app
