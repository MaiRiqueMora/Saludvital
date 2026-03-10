"""
Vistas basadas en clases para las páginas HTML (templates) del sistema.

Incluye listas con paginación, formularios de creación/edición y
soporte de filtros mediante parámetros GET (selects en las plantillas).
"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.urls import reverse_lazy
from .models import (
    Especialidad, Paciente, Medico, ConsultaMedica,
    Tratamiento, RecetaMedica, Laboratorio, Medicamento, HistoriaClinica
)

def apply_search(queryset, model_cls, term):
    """Aplica búsqueda libre sobre campos de texto y enteros exactos.

    - Para Char/Text/Email usa icontains
    - Para enteros, si el término es dígito, filtra por igualdad
    """
    if not term:
        return queryset
    query = Q()
    for field in model_cls._meta.get_fields():
        internal = getattr(field, 'get_internal_type', None)
        if not internal:
            continue
        ftype = field.get_internal_type()
        if ftype in ['CharField', 'TextField', 'EmailField']:
            query |= Q(**{f"{field.name}__icontains": term})
        elif ftype in ['IntegerField', 'PositiveIntegerField', 'BigIntegerField'] and term.isdigit():
            query |= Q(**{field.name: int(term)})
    return queryset.filter(query)


class EspecialidadListView(ListView):
    """Lista de especialidades con búsqueda libre."""
    model = Especialidad; template_name = 'especialidad_lista.html'; paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get('q', '').strip()
        return apply_search(qs, self.model, term)
class EspecialidadCreateView(CreateView):
    model = Especialidad; fields='__all__'; success_url=reverse_lazy('especialidad_list'); template_name='especialidad_form.html'
class EspecialidadUpdateView(UpdateView):
    model = Especialidad; fields='__all__'; success_url=reverse_lazy('especialidad_list'); template_name='especialidad_form.html'
class EspecialidadDeleteView(DeleteView):
    model = Especialidad; success_url=reverse_lazy('especialidad_list'); template_name='especialidad_confirmar_borrar.html'

class PacienteListView(ListView):
    """Lista de pacientes con filtros por tipo de sangre y estado activo."""
    model = Paciente; template_name = 'paciente_lista.html'; paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get('q', '').strip()
        qs = apply_search(qs, self.model, term)
        tipo = self.request.GET.get('tipo_sangre')
        if tipo:
            qs = qs.filter(tipo_sangre=tipo)
        activo = self.request.GET.get('activo')
        if activo in ['true','false']:
            qs = qs.filter(activo=(activo == 'true'))
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tipos_sangre'] = getattr(self.model, 'TIPO_SANGRE', None) or []
        ctx['TIPO_SANGRE'] = [('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-')]
        ctx['f_activo'] = self.request.GET.get('activo','')
        ctx['f_tipo_sangre'] = self.request.GET.get('tipo_sangre','')
        return ctx
class PacienteCreateView(CreateView):
    model = Paciente; fields='__all__'; success_url=reverse_lazy('paciente_list'); template_name='paciente_form.html'
class PacienteUpdateView(UpdateView):
    model = Paciente; fields='__all__'; success_url=reverse_lazy('paciente_list'); template_name='paciente_form.html'
class PacienteDeleteView(DeleteView):
    model = Paciente; success_url=reverse_lazy('paciente_list'); template_name='paciente_confirmar_borrar.html'

class MedicoListView(ListView):
    """Lista de médicos con filtros por especialidad y estado activo."""
    model = Medico; template_name = 'medico_lista.html'; paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get('q', '').strip()
        qs = apply_search(qs, self.model, term)
        esp_id = self.request.GET.get('especialidad')
        if esp_id:
            qs = qs.filter(especialidad_id=esp_id)
        activo = self.request.GET.get('activo')
        if activo in ['true','false']:
            qs = qs.filter(activo=(activo == 'true'))
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['especialidades'] = Especialidad.objects.all()
        ctx['f_especialidad'] = self.request.GET.get('especialidad','')
        ctx['f_activo'] = self.request.GET.get('activo','')
        return ctx
class MedicoCreateView(CreateView):
    model = Medico; fields='__all__'; success_url=reverse_lazy('medico_list'); template_name='medico_form.html'
class MedicoUpdateView(UpdateView):
    model = Medico; fields='__all__'; success_url=reverse_lazy('medico_list'); template_name='medico_form.html'
class MedicoDeleteView(DeleteView):
    model = Medico; success_url=reverse_lazy('medico_list'); template_name='medico_confirmar_borrar.html'

class ConsultaListView(ListView):
    """Lista de consultas con filtros por estado, médico y paciente."""
    model = ConsultaMedica; template_name = 'consulta_lista.html'; paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get('q', '').strip()
        qs = apply_search(qs, self.model, term)
        estado = self.request.GET.get('estado')
        if estado:
            qs = qs.filter(estado=estado)
        medico_id = self.request.GET.get('medico')
        if medico_id:
            qs = qs.filter(medico_id=medico_id)
        paciente_id = self.request.GET.get('paciente')
        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['estados'] = [('PEND','Pendiente'),('ATND','Atendida'),('CANCEL','Cancelada')]
        ctx['medicos'] = Medico.objects.all()
        ctx['pacientes'] = Paciente.objects.all()
        ctx['f_estado'] = self.request.GET.get('estado','')
        ctx['f_medico'] = self.request.GET.get('medico','')
        ctx['f_paciente'] = self.request.GET.get('paciente','')
        return ctx
class ConsultaCreateView(CreateView):
    model = ConsultaMedica; fields='__all__'; success_url=reverse_lazy('consulta_list'); template_name='consulta_form.html'
class ConsultaUpdateView(UpdateView):
    model = ConsultaMedica; fields='__all__'; success_url=reverse_lazy('consulta_list'); template_name='consulta_form.html'
class ConsultaDeleteView(DeleteView):
    model = ConsultaMedica; success_url=reverse_lazy('consulta_list'); template_name='consulta_confirmar_borrar.html'

class TratamientoListView(ListView):
    """Lista de tratamientos con filtro por consulta asociada."""
    model = Tratamiento; template_name = 'tratamiento_lista.html'; paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get('q', '').strip()
        qs = apply_search(qs, self.model, term)
        consulta_id = self.request.GET.get('consulta')
        if consulta_id:
            qs = qs.filter(consulta_id=consulta_id)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['consultas'] = ConsultaMedica.objects.all()
        ctx['f_consulta'] = self.request.GET.get('consulta','')
        return ctx
class TratamientoCreateView(CreateView):
    model = Tratamiento; fields='__all__'; success_url=reverse_lazy('tratamiento_list'); template_name='tratamiento_form.html'
class TratamientoUpdateView(UpdateView):
    model = Tratamiento; fields='__all__'; success_url=reverse_lazy('tratamiento_list'); template_name='tratamiento_form.html'
class TratamientoDeleteView(DeleteView):
    model = Tratamiento; success_url=reverse_lazy('tratamiento_list'); template_name='tratamiento_confirmar_borrar.html'

class RecetaListView(ListView):
    """Lista de recetas con filtros por medicamento y tratamiento."""
    model = RecetaMedica; template_name = 'receta_lista.html'; paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get('q', '').strip()
        qs = apply_search(qs, self.model, term)
        medicamento_id = self.request.GET.get('medicamento')
        if medicamento_id:
            qs = qs.filter(medicamento_id=medicamento_id)
        tratamiento_id = self.request.GET.get('tratamiento')
        if tratamiento_id:
            qs = qs.filter(tratamiento_id=tratamiento_id)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['medicamentos'] = Medicamento.objects.all()
        ctx['tratamientos'] = Tratamiento.objects.all()
        ctx['f_medicamento'] = self.request.GET.get('medicamento','')
        ctx['f_tratamiento'] = self.request.GET.get('tratamiento','')
        return ctx
class RecetaCreateView(CreateView):
    model = RecetaMedica; fields='__all__'; success_url=reverse_lazy('receta_list'); template_name='receta_form.html'
class RecetaUpdateView(UpdateView):
    model = RecetaMedica; fields='__all__'; success_url=reverse_lazy('receta_list'); template_name='receta_form.html'
class RecetaDeleteView(DeleteView):
    model = RecetaMedica; success_url=reverse_lazy('receta_list'); template_name='receta_confirmar_borrar.html'

class LaboratorioListView(ListView):
    """Lista de laboratorios con búsqueda libre (nombre/teléfono)."""
    model = Laboratorio; template_name = 'laboratorio_lista.html'; paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get('q', '').strip()
        return apply_search(qs, self.model, term)
class LaboratorioCreateView(CreateView):
    model = Laboratorio; fields='__all__'; success_url=reverse_lazy('laboratorio_list'); template_name='laboratorio_form.html'
class LaboratorioUpdateView(UpdateView):
    model = Laboratorio; fields='__all__'; success_url=reverse_lazy('laboratorio_list'); template_name='laboratorio_form.html'
class LaboratorioDeleteView(DeleteView):
    model = Laboratorio; success_url=reverse_lazy('laboratorio_list'); template_name='laboratorio_confirmar_borrar.html'

class MedicamentoListView(ListView):
    """Lista de medicamentos con filtro por laboratorio y búsqueda libre."""
    model = Medicamento; template_name = 'medicamento_lista.html'; paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get('q', '').strip()
        qs = apply_search(qs, self.model, term)
        laboratorio_id = self.request.GET.get('laboratorio')
        if laboratorio_id:
            qs = qs.filter(laboratorio_id=laboratorio_id)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['laboratorios'] = Laboratorio.objects.all()
        ctx['f_laboratorio'] = self.request.GET.get('laboratorio','')
        return ctx
class MedicamentoCreateView(CreateView):
    model = Medicamento; fields='__all__'; success_url=reverse_lazy('medicamento_list'); template_name='medicamento_form.html'
class MedicamentoUpdateView(UpdateView):
    model = Medicamento; fields='__all__'; success_url=reverse_lazy('medicamento_list'); template_name='medicamento_form.html'
class MedicamentoDeleteView(DeleteView):
    model = Medicamento; success_url=reverse_lazy('medicamento_list'); template_name='medicamento_confirmar_borrar.html'

class HistoriaListView(ListView):
    """Lista de historias clínicas con filtro por paciente."""
    model = HistoriaClinica; template_name = 'historia_lista.html'; paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get('q', '').strip()
        qs = apply_search(qs, self.model, term)
        paciente_id = self.request.GET.get('paciente')
        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pacientes'] = Paciente.objects.all()
        ctx['f_paciente'] = self.request.GET.get('paciente','')
        return ctx
class HistoriaCreateView(CreateView):
    model = HistoriaClinica; fields='__all__'; success_url=reverse_lazy('historia_list'); template_name='historia_form.html'
class HistoriaUpdateView(UpdateView):
    model = HistoriaClinica; fields='__all__'; success_url=reverse_lazy('historia_list'); template_name='historia_form.html'
class HistoriaDeleteView(DeleteView):
    model = HistoriaClinica; success_url=reverse_lazy('historia_list'); template_name='historia_confirmar_borrar.html'

class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Estadísticas básicas para el dashboard
        ctx['stats'] = {
            'pacientes': Paciente.objects.count(),
            'medicos': Medico.objects.count(),
            'consultas': ConsultaMedica.objects.count(),
            'especialidades': Especialidad.objects.count(),
            'medicamentos': Medicamento.objects.count(),
            'laboratorios': Laboratorio.objects.count(),
        }
        return ctx