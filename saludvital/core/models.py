"""
Modelos de datos para el sistema Salud Vital Ltda.

Este módulo contiene todas las entidades del sistema de gestión médica:
- Especialidad: Especialidades médicas disponibles
- Paciente: Información de pacientes de la clínica
- Medico: Información de médicos y sus especialidades
- ConsultaMedica: Registro de consultas médicas
- Tratamiento: Tratamientos prescritos en consultas
- Laboratorio: Laboratorios farmacéuticos
- Medicamento: Medicamentos disponibles
- RecetaMedica: Recetas médicas con medicamentos
- HistoriaClinica: Historial clínico de pacientes

Autor: Sistema Salud Vital
Sección: AP-173
Año: 2025
"""

from django.db import models

class Especialidad(models.Model):
    """
    Modelo para las especialidades médicas disponibles en la clínica.
    
    Campos:
    - nombre: Nombre de la especialidad médica
    - descripcion: Descripción detallada de la especialidad
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    def __str__(self): return self.nombre

TIPO_SANGRE = [
    ('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),
    ('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-'),
]

ESTADO_CONSULTA = [
    ('PEND','Pendiente'),
    ('ATND','Atendida'),
    ('CANCEL','Cancelada'),
]

class Paciente(models.Model):
    """
    Modelo para la información de pacientes de la clínica.
    
    Campos:
    - rut: RUT único del paciente
    - nombre: Nombre del paciente
    - apellido: Apellido del paciente
    - fecha_nacimiento: Fecha de nacimiento
    - tipo_sangre: Tipo de sangre (CHOICES)
    - correo: Correo electrónico
    - telefono: Teléfono de contacto
    - direccion: Dirección del paciente
    - activo: Estado activo/inactivo del paciente
    """
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    tipo_sangre = models.CharField(max_length=3, choices=TIPO_SANGRE)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=250, blank=True)
    activo = models.BooleanField(default=True)
    def __str__(self): return f"{self.nombre} {self.apellido}"

class Medico(models.Model):
    """
    Modelo para la información de médicos de la clínica.
    
    Campos:
    - nombre: Nombre del médico
    - apellido: Apellido del médico
    - rut: RUT único del médico
    - correo: Correo electrónico
    - telefono: Teléfono de contacto
    - activo: Estado activo/inactivo del médico
    - especialidad: Especialidad médica (FK)
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True, related_name='medicos')
    def __str__(self): return f"Dr. {self.nombre} {self.apellido}"

class ConsultaMedica(models.Model):
    """
    Modelo para el registro de consultas médicas.
    
    Campos:
    - paciente: Paciente atendido (FK)
    - medico: Médico que atiende (FK)
    - fecha_consulta: Fecha y hora de la consulta
    - motivo: Motivo de la consulta
    - diagnostico: Diagnóstico médico
    - estado: Estado de la consulta (CHOICES)
    """
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, related_name='consultas')
    fecha_consulta = models.DateTimeField()
    motivo = models.TextField()
    diagnostico = models.TextField(blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CONSULTA, default='PEND')
    def __str__(self): return f"Consulta {self.id} - {self.paciente}"

class Tratamiento(models.Model):
    """
    Modelo para los tratamientos prescritos en consultas.
    
    Campos:
    - consulta: Consulta médica asociada (FK)
    - descripcion: Descripción del tratamiento
    - duracion_dias: Duración en días
    - observaciones: Observaciones adicionales
    """
    consulta = models.ForeignKey(ConsultaMedica, on_delete=models.CASCADE, related_name='tratamientos')
    descripcion = models.TextField()
    duracion_dias = models.IntegerField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    def __str__(self): return f"Tratamiento {self.id} para consulta {self.consulta.id}"

class Laboratorio(models.Model):
    """
    Modelo para laboratorios farmacéuticos.
    
    Campos:
    - nombre: Nombre del laboratorio
    - direccion: Dirección del laboratorio
    - telefono: Teléfono de contacto
    """
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    def __str__(self): return self.nombre

class Medicamento(models.Model):
    """
    Modelo para medicamentos disponibles.
    
    Campos:
    - nombre: Nombre del medicamento
    - laboratorio: Laboratorio fabricante (FK)
    - stock: Cantidad en stock
    - precio_unitario: Precio por unidad
    """
    nombre = models.CharField(max_length=200)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self): return self.nombre

class RecetaMedica(models.Model):
    """
    Modelo para recetas médicas con medicamentos.
    
    Campos:
    - tratamiento: Tratamiento asociado (FK)
    - medicamento: Medicamento prescrito (FK)
    - dosis: Dosis del medicamento
    - frecuencia: Frecuencia de administración
    - duracion: Duración del tratamiento
    """
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, related_name='recetas')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    duracion = models.CharField(max_length=100)
    def __str__(self): return f"Receta {self.id} - {self.medicamento.nombre}"

class HistoriaClinica(models.Model):
    """
    Modelo para el historial clínico de pacientes.
    
    Campos:
    - paciente: Paciente asociado (FK)
    - resumen: Resumen del historial clínico
    - creada: Fecha de creación automática
    """
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historias')
    resumen = models.TextField()
    creada = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Historia {self.id} - {self.paciente}"