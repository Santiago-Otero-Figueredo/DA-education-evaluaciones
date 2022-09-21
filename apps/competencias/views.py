from django.shortcuts import render

from django.views.generic import ListView

from apps.competencias.models import Grupo, ProfesorCursoPrograma
from apps.evaluaciones.models import Actividad
# Create your views here.

# Grupos

class ListadoGruposProfesorCursoPrograma(ListView):
    model = Grupo
    context_object_name = 'grupos'
    template_name = "competencias/grupos/listado_por_profesor_curso_programa.html"

    def get_queryset(self):
        profesor_curso_programa_id = self.kwargs.pop('id_profesor_curso_programa', 0)
        self.profesor_curso_programa = ProfesorCursoPrograma.obtener_por_id(profesor_curso_programa_id)
        return Grupo.obtener_grupos_de_profesor_curso_programa(profesor_curso_programa_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profesor_curso_programa'] = self.profesor_curso_programa

        return context

