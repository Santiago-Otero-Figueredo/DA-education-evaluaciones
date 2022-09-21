from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.views.generic import FormView, CreateView, ListView

from apps.evaluaciones.forms import NotaEstudianteCualitativoForm, NotaEstudianteCuantitativoForm, notas_cuantitativas_formset, notas_cualitativas_formset

from apps.competencias.models import Grupo, ProfesorCursoPrograma
from apps.evaluaciones.models import Actividad, Nota
from apps.usuarios.models import Usuario


# Create your views here.

class ListadoEvaluacionesProfesorCursoPrograma(ListView):
    model = Actividad
    context_object_name = 'actividades'
    template_name = "evaluaciones/listado_por_profesor_curso_programa.html"

    def get_queryset(self):
        profesor_curso_programa_id = self.kwargs.pop('id_profesor_curso_programa', 0)
        grupo_id = self.kwargs.pop('id_grupo', 0)
        self.grupo = Grupo.obtener_por_id(grupo_id)
        self.profesor_curso_programa = ProfesorCursoPrograma.obtener_por_id(profesor_curso_programa_id)
        return self.profesor_curso_programa.obtener_actividades()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profesor_curso_programa'] = self.profesor_curso_programa
        context['grupo'] = self.grupo

        return context


class EstudiantesPorEvaluacion(ListView):
    model = Usuario
    context_object_name = 'estudiantes_grupo'
    template_name = 'evaluaciones/estudiantes_por_evaluacion.html'

    def get_queryset(self):
        id_grupo = self.kwargs.pop('id_grupo', 0)
        id_profesor_curso_programa = self.kwargs.pop('id_profesor_curso_programa', 0)
        id_actividad = self.kwargs.pop('id_actividad', 0)

        self.actividad = Actividad.obtener_por_id(id_actividad)
        self.profesor_curso_programa = ProfesorCursoPrograma.obtener_por_id(id_profesor_curso_programa)
        self.grupo = Grupo.obtener_por_id(id_grupo)
        return self.grupo.estudiantes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['grupo'] = self.grupo
        context['profesor_curso_programa'] = self.profesor_curso_programa
        context['actividad'] = self.actividad

        return context


class CalificarEvaluacionesEstudiantes(FormView):
    template_name = 'evaluaciones/calificar_preguntas_estudiante.html'

    def dispatch(self, request, *args, **kwargs):
        id_actividad = self.kwargs.pop('id_actividad', 0)
        id_estudiante = self.kwargs.pop('id_estudiante', 0)
        id_grupo = self.kwargs.pop('id_grupo', 0)

        self.actividad = Actividad.obtener_por_id(id_actividad)
        self.estudiante = Usuario.obtener_por_id(id_estudiante)
        self.grupo = Grupo.obtener_por_id(id_grupo)
        self.preguntas = self.actividad.preguntas_asociadas.all()

        self.formset_notas = self.get_formset_class()(form_kwargs={'estudiante':self.estudiante}, queryset=self.preguntas, prefix="pregunta")

        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.actividad.tipo_calificacion=='Cuantitativa':
            return NotaEstudianteCuantitativoForm
        return NotaEstudianteCualitativoForm

    def get_formset_class(self):
        if self.actividad.tipo_calificacion=='Cuantitativa':
            return notas_cuantitativas_formset
        return notas_cualitativas_formset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['estudiante'] = self.estudiante
        context['preguntas'] = self.preguntas
        context['actividad'] = self.actividad
        context['grupo'] = self.grupo
        context['formset'] = self.formset_notas

        return context


    def post(self, *args, **kwargs):

        formset = self.get_formset_class()(self.request.POST, form_kwargs={'empty_permitted': False, 'estudiante':self.estudiante}, prefix="pregunta")

        if formset.is_valid():
            return self.form_valid(formset)
        else:
            errores = ''
            for form in formset:
                for _, errors in form.errors.items():
                    print("#errores: ",errors)
                    errores += ('{}'.format(','.join(errors)))

            print("# errores: ", errores)
            return HttpResponseRedirect(self.request.path_info)


    def form_valid(self, formset):
        try:
            for form in formset:
                pregunta = form.save(commit=False)

                resultado = 0.0
                calificacion_cualitativa = None

                if self.actividad.tipo_calificacion=='Cuantitativa':
                    resultado = form.cleaned_data['resultado']
                else:
                    calificacion_cualitativa = form.cleaned_data['calificacion_cualitativa']


                if Nota.existe_por_estudiante_y_pregunta(self.estudiante.pk, pregunta.pk) is True:
                    nota = Nota.obtener_por_estudiante_y_pregunta(self.estudiante.pk, pregunta.pk)
                    nota.resultado = resultado
                    nota.calificacion_cualitativa = calificacion_cualitativa
                    nota.save()
                else:
                    Nota.objects.create(
                        calificacion_cualitativa = calificacion_cualitativa,
                        pregunta = pregunta,
                        estudiante = self.estudiante,
                        resultado = resultado
                    )

                pregunta.save()

            messages.success(self.request, "Calificaciones registradas correctamente")
        except:
            messages.error(self.request, "Ha ocurrido un error al registrar las calificaciones")
        finally:
            return HttpResponseRedirect(self.request.path_info)
