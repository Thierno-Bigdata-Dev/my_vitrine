FROM python:3.11-slim

# Empêcher Python d'écrire des fichiers .pyc et forcer l'affichage des logs en temps réel
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copier et installer les dépendances
COPY senegal_commerce/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY senegal_commerce/ /app/

# Exposer le port de Django
EXPOSE 8000

# Lancer le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
