"""Configuración de la aplicación `core`.

Se usa para ajustar metadatos y señales si fuese necesario.
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
