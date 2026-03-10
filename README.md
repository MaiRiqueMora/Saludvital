Salud Vital Ltda. – Backend (Django + DRF)

Introducción
Proyecto de backend para la clínica Salud Vital Ltda. Incluye modelos interrelacionados, CRUD con templates (fuera del admin), API REST con DRF, filtros en vistas y API, y documentación Swagger.

Requisitos
- Windows 10/11
- Python 3.13 (o 3.11+)

Entorno virtual (eva2)
1. Crear (si no existe):
   python -m venv eva2
2. Usar sin activar (recomendado en PowerShell con políticas restrictivas):
   .\eva2\Scripts\python.exe --version

Instalación de dependencias
Las dependencias están ya en el entorno local (carpeta eva2). Si necesitas reinstalar:
   .\eva2\Scripts\pip.exe install -U pip
   .\eva2\Scripts\pip.exe install django djangorestframework django-filter drf-yasg python-decouple psycopg2-binary sqlparse pytz tzdata

Configuración
El proyecto está configurado para SQLite por defecto (no requiere servidor externo).
Archivo: saludvital/saludvital/settings.py

Migraciones y BD
   .\eva2\Scripts\python.exe .\saludvital\manage.py migrate

Cargar datos de ejemplo (fixtures)
   .\eva2\Scripts\python.exe .\saludvital\manage.py loaddata core/fixtures/initial_data.json
   .\eva2\Scripts\python.exe .\saludvital\manage.py loaddata core/fixtures/extra_data.json

Crear superusuario (admin)
   .\eva2\Scripts\python.exe .\saludvital\manage.py createsuperuser

Ejecutar servidor
   .\eva2\Scripts\python.exe .\saludvital\manage.py runserver

URLs principales
- Home: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Templates CRUD:
  - /especialidades/, /pacientes/, /medicos/, /consultas/, /tratamientos/, /recetas/, /laboratorios/, /medicamentos/, /historias/
- API REST (DRF): http://127.0.0.1:8000/api/
- Swagger (docs): http://127.0.0.1:8000/swagger/

Filtros en templates
- Pacientes: tipo de sangre, activo
- Médicos: especialidad, activo
- Consultas: estado, médico, paciente
- Tratamientos: consulta
- Recetas: medicamento, tratamiento
- Medicamentos: laboratorio

Filtros en API (DRF)
Endpoints de /api/ soportan parámetros de filtro definidos con django-filter (ver core/views.py).

Notas
- Si tu PowerShell bloquea la activación del entorno, puedes ejecutar los binarios directamente como se muestra arriba.
- PostgreSQL no es requerido para ejecutar esta versión (está en SQLite). Si deseas usar Postgres, ajusta variables con python-decouple y cambia el ENGINE en settings.py.

Créditos
- Desarrollado por: Maite Riquelme Morales – Sección AP-173 – 2025

