"""
Vistas de API REST para el sistema Salud Vital Ltda.

Este módulo contiene todas las vistas de API usando Django REST Framework:
- ViewSets para cada entidad del sistema
- Filtros aplicados a campos clave
- Serialización de datos para la API

Autor: Sistema Salud Vital
Sección: AP-173
Año: 2025
"""

from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *


# Create your views here.
class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre']

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rut','nombre','apellido','tipo_sangre']

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['especialidad','activo','rut']

class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = ConsultaMedica.objects.all()
    serializer_class = ConsultaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['medico','paciente','fecha_consulta','estado']

class TratamientoViewSet(viewsets.ModelViewSet):
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer

class LaboratorioViewSet(viewsets.ModelViewSet):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer

class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['laboratorio','nombre']

class RecetaViewSet(viewsets.ModelViewSet):
    queryset = RecetaMedica.objects.all()
    serializer_class = RecetaSerializer

class HistoriaViewSet(viewsets.ModelViewSet):
    queryset = HistoriaClinica.objects.all()
    serializer_class = HistoriaSerializer