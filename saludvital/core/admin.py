"""Configuración del sitio de administración de Django para Salud Vital.

Define listas, filtros y búsquedas para acelerar la gestión de datos.
"""
from django.contrib import admin
from .models import (
    Especialidad, Paciente, Medico, ConsultaMedica,
    Tratamiento, Laboratorio, Medicamento,
    RecetaMedica, HistoriaClinica
)

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("rut", "nombre", "apellido", "tipo_sangre", "activo")
    search_fields = ("rut", "nombre", "apellido")
    list_filter = ("tipo_sangre", "activo")

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ("rut", "nombre", "apellido", "especialidad", "activo")
    search_fields = ("rut", "nombre", "apellido")
    list_filter = ("especialidad", "activo")

@admin.register(ConsultaMedica)
class ConsultaMedicaAdmin(admin.ModelAdmin):
    list_display = ("id", "paciente", "medico", "fecha_consulta", "estado")
    list_filter = ("estado", "fecha_consulta")

@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    list_display = ("id", "consulta", "duracion_dias")

@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "laboratorio", "stock", "precio_unitario")
    search_fields = ("nombre",)

@admin.register(RecetaMedica)
class RecetaMedicaAdmin(admin.ModelAdmin):
    list_display = ("id", "tratamiento", "medicamento", "dosis")

@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ("id", "paciente", "creada")
