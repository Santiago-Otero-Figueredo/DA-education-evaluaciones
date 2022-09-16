from django.views.generic import ListView, TemplateView, FormView
from apps.competencias.models import NivelEvaluacion, ProfesorCursoPrograma, TipoNivelEvaluacion

from apps.dashboards.models import Reporte
from apps.matriculas.models import Matricula
from apps.periodos_academicos.models import PeriodoAcademico
from apps.programas.models import Programa
from apps.cursos.models import Curso, CursoDelPrograma

from apps.dashboards.forms import FiltroPeriodoProgramaForm, FiltroNivelesEvaluacionPorProfesorForm, FiltroProgramaForm
from apps.usuarios.models import Usuario

class Inicio(TemplateView):
    template_name = "dashboard/inicio.html"

class CursosEvaluacion(FormView):
    model = Reporte
    form_class = FiltroPeriodoProgramaForm
    template_name = "dashboard/cusos_programa_periodo_academico.html"

    def dispatch(self, request, *args, **kwargs):

        self.ano = request.GET.get('ano', 2022)
        self.periodos_academicos = request.GET.getlist('periodo_academico', PeriodoAcademico.obtener_periodos_academicos_por_ano(self.ano))
        self.programa = request.GET.get('programa', Programa.obtener_activos().first())

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['periodos_academicos'] = PeriodoAcademico.obtener_periodos_academicos_por_ano_y_lista_ids(self.ano, self.periodos_academicos)
        context['ano'] = self.ano
        context['programa'] = self.programa

        return context

    def get_initial(self):
        initial = super().get_initial()

        initial["programa"] = self.programa
        initial["periodo_academico"] = self.periodos_academicos
        initial["ano"] = self.ano

        return initial

class ResumenNivelesEvaluacion(ListView):
    model = Reporte
    context_object_name = "niveles_evaluacion"
    template_name = "dashboard/resumen_niveles_evaluacion.html"


    def get_queryset(self):
        id_curso = self.kwargs.pop("id_curso", 0)
        id_periodo_academico = self.kwargs.pop("periodo_academico", 0)
        self.curso = Curso.obtener_por_id(id_curso)
        self.periodo_academico = PeriodoAcademico.obtener_por_id(id_periodo_academico)

        return NivelEvaluacion.obtener_nivel_evaluacion_por_curso(id_curso)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['tipos'] = TipoNivelEvaluacion.obtener_activos()
        context['curso'] = self.curso
        context['periodo_academico'] = self.periodo_academico

        return context


class ResumenNivelesEvaluacionPorProfesor(FormView):
    model = Reporte
    form_class = FiltroNivelesEvaluacionPorProfesorForm
    template_name = "dashboard/resumen_niveles_evaluacion.html"

    def dispatch(self, request, *args, **kwargs):

        self.id_curso = self.kwargs.pop('id_curso', 0)
        self.id_periodo_academico = self.kwargs.pop('id_periodo_academico', 0)

        self.ano = request.GET.get('ano', 2022)
        self.periodo_academico = request.GET.get('periodo_academico', PeriodoAcademico.obtener_periodos_academicos_por_ano(self.ano).first().pk)

        self.programa = request.GET.get('programa', Programa.obtener_activos().first().pk)
        self.curso_del_programa = CursoDelPrograma.obtener_por_curso_programa_id(self.id_curso, self.programa).pk

        self.profesor = request.GET.get('profesor', 0)

        self.profesor_curso_del_programa = ProfesorCursoPrograma.obtener_por_curso_del_programa_profesor_y_periodo_academico(
            id_curso_del_programa = self.curso_del_programa,
            id_periodo_academico = self.periodo_academico,
            id_profesor = self.profesor
        )


        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['periodo_academico'] = self.periodo_academico
        context['ano'] = self.ano
        context['programa'] = self.programa
        context['profesor'] = self.profesor
        context['tipos'] = TipoNivelEvaluacion.obtener_activos()
        context['profesor_curso_del_programa'] = self.profesor_curso_del_programa

        if self.profesor == 0 or self.profesor == '':
            niveles_evaluacion = NivelEvaluacion.obtener_por_curso_del_programa_y_periodo_academico(
                id_curso_programa=self.curso_del_programa,
                id_periodo_academico=self.periodo_academico
            )
        else:
            niveles_evaluacion = NivelEvaluacion.obtener_nivel_evaluacion_por_curso_del_programa_periodo_profesor(
                id_curso_programa=self.curso_del_programa,
                id_periodo_academico=self.periodo_academico,
                id_profesor=self.profesor
            )

        context['niveles_evaluacion'] = niveles_evaluacion


        return context

    def get_initial(self):
        initial = super().get_initial()

        initial["programa"] = self.programa
        initial["periodo_academico"] = self.periodo_academico
        initial["ano"] = self.ano
        initial['profesor'] = self.profesor

        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['id_curso_del_programa'] = self.curso_del_programa
        return kwargs


class ResumenCalificaciones(ListView):
    model = Reporte
    context_object_name = "respuestas"
    template_name = "dashboard/resumen_calificaciones.html"


    def get_queryset(self):
        id_estudiante = self.kwargs.pop('id_estudiante', 0)
        id_profesor_curso_programa = self.kwargs.pop('id_profesor_curso_programa', 0)
        self.curso = ProfesorCursoPrograma.obtener_por_id(id_profesor_curso_programa).curso_programa.curso
        self.estudiante = Usuario.obtener_por_id(id_estudiante)
        return self.estudiante.obtener_respuestas_estudiante(id_profesor_curso_programa)


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['tipo'] = TipoNivelEvaluacion.obtener_ultimo_tipo()
        context['curso'] = self.curso
        context['estudiante'] = self.estudiante

        return context

class ResumenCalificacionesPorEvaluacion(ListView):
    model = Reporte
    context_object_name = "respuestas"
    template_name = "dashboard/resumen_calificaciones_por_evaluaciones.html"


    def get_queryset(self):
        id_estudiante = self.kwargs.pop('id_estudiante', 0)
        self.id_profesor_curso_programa = self.kwargs.pop('id_profesor_curso_programa', 0)
        self.curso = ProfesorCursoPrograma.obtener_por_id(self.id_profesor_curso_programa).curso_programa.curso
        self.estudiante = Usuario.obtener_por_id(id_estudiante)
        return self.estudiante.obtener_respuestas_estudiante_por_evaluacion(self.id_profesor_curso_programa)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['tipo'] = TipoNivelEvaluacion.obtener_ultimo_tipo()
        context['curso'] = self.curso
        context['estudiante'] = self.estudiante
        context['id_profesor_curso_programa'] = self.id_profesor_curso_programa
        return context


class CursosPorEstudiante(FormView):
    model = Reporte
    form_class = FiltroPeriodoProgramaForm
    template_name = "dashboard/cusos_por_estudiante.html"

    def dispatch(self, request, *args, **kwargs):

        self.estudiante = self.kwargs.pop('id_estudiante', 0)
        self.ano = request.GET.get('ano', 2022)
        self.periodos_academicos = request.GET.getlist('periodo_academico', PeriodoAcademico.obtener_periodos_academicos_por_ano(self.ano))
        self.programa = request.GET.get('programa', Programa.obtener_programas_por_estudiante(self.estudiante).first())

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['periodos_academicos'] = PeriodoAcademico.obtener_periodos_academicos_por_ano_y_lista_ids(self.ano, self.periodos_academicos)
        context['ano'] = self.ano
        context['programa'] = self.programa
        context['estudiante'] = Usuario.obtener_por_id(self.estudiante)

        return context

    def get_initial(self):
        initial = super().get_initial()

        initial["programa"] = self.programa
        initial["periodo_academico"] = self.periodos_academicos
        initial["ano"] = self.ano

        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['id_estudiante'] = self.estudiante
        return kwargs
