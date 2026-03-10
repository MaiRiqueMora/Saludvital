"""
URL configuration for saludvital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers
from core.views import (
    EspecialidadViewSet, PacienteViewSet, MedicoViewSet, ConsultaViewSet,
    TratamientoViewSet, LaboratorioViewSet, MedicamentoViewSet, 
    RecetaViewSet, HistoriaViewSet
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(openapi.Info(title="Salud Vital API", default_version='v1'), public=True)


router = routers.DefaultRouter()
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'medicos', MedicoViewSet)
router.register(r'consultas', ConsultaViewSet)
router.register(r'tratamientos', TratamientoViewSet)
router.register(r'laboratorios', LaboratorioViewSet)
router.register(r'medicamentos', MedicamentoViewSet)
router.register(r'recetas', RecetaViewSet)
router.register(r'historias', HistoriaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('core.urls')),
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('', RedirectView.as_view(pattern_name='schema-swagger-ui', permanent=False)),
]

 
