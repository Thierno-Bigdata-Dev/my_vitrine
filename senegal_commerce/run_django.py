#!/usr/bin/env python
"""
Script pour lancer l'application Django Sénégal Commerce
"""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senegal_commerce.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Démarrer le serveur de développement
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])