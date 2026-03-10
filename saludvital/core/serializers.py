"""
Serializers para el sistema Salud Vital Ltda.

Este módulo contiene todos los serializers de Django REST Framework:
- Serialización de modelos para la API
- Conversión entre objetos Python y JSON
- Validación de datos de entrada

Autor: Sistema Salud Vital
Sección: AP-173
Año: 2025
"""

from rest_framework import serializers
from .models import *
class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta: model = Especialidad; fields='__all__'
class PacienteSerializer(serializers.ModelSerializer):
    class Meta: model = Paciente; fields='__all__'
class MedicoSerializer(serializers.ModelSerializer):
    class Meta: model = Medico; fields='__all__'
class ConsultaSerializer(serializers.ModelSerializer):
    class Meta: model = ConsultaMedica; fields='__all__'
class TratamientoSerializer(serializers.ModelSerializer):
    class Meta: model = Tratamiento; fields='__all__'
class LaboratorioSerializer(serializers.ModelSerializer):
    class Meta: model = Laboratorio; fields='__all__'
class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta: model = Medicamento; fields='__all__'
class RecetaSerializer(serializers.ModelSerializer):
    class Meta: model = RecetaMedica; fields='__all__'
class HistoriaSerializer(serializers.ModelSerializer):
    class Meta: model = HistoriaClinica; fields='__all__'