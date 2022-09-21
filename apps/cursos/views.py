from django.shortcuts import render

from django.views.generic import FormView

from apps.usuarios.models import Usuario

from apps.cursos.models import Curso
from apps.periodos_academicos.models import PeriodoAcademico
from apps.programas.models import Programa

from apps.cursos.forms import FiltroPrograma

class CursosAsigandosActualmente(FormView):
    model = Curso
    form_class = FiltroPrograma
    template_name = "cursos/cursos_por_profesor.html"

    def dispatch(self, request, *args, **kwargs):

        id_profesor = self.kwargs.pop('id_profesor', 0)
        self.profesor = Usuario.obtener_profesores().get(pk=id_profesor)
        self.periodo_academico = PeriodoAcademico.obtener_activo()
        self.programa = request.GET.get('programa', Programa.obtener_programas_por_profesor_y_periodo_academico(self.profesor.pk, self.periodo_academico.pk).first())


        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.programa is None:
            cursos = Curso.objects.none()
        else:
            cursos = Curso.obtener_cursos_por_profesor_periodo_academico_y_programa(
                id_profesor=self.profesor.pk,
                id_periodo_academico=self.periodo_academico.pk,
                id_programa=self.programa.pk
            )

        context['cursos'] = cursos
        context['profesor'] = self.profesor
        context['periodo_academico'] = self.periodo_academico
        context['programa'] = self.programa

        return context

    def get_initial(self):
        initial = super().get_initial()

        initial["programas"] = self.programa

        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['programas'] = Programa.obtener_programas_por_profesor_y_periodo_academico(self.profesor.pk, self.periodo_academico.pk)
        return kwargs