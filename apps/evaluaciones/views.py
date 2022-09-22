from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.views.generic import FormView, CreateView, ListView

from apps.evaluaciones.forms import NotaEstudianteCualitativoForm, NotaEstudianteCuantitativoForm

from apps.competencias.models import Grupo, ProfesorCursoPrograma
from apps.evaluaciones.models import Actividad, CalificacionCualitativa, Nota, Pregunta
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


class CalificarEvaluacionesEstudiantes(FormView):
    template_name = 'evaluaciones/calificar_preguntas_estudiante.html'

    def dispatch(self, request, *args, **kwargs):
        id_actividad = self.kwargs.pop('id_actividad', 0)
        id_grupo = self.kwargs.pop('id_grupo', 0)

        self.actividad = Actividad.obtener_por_id(id_actividad)
        self.grupo = Grupo.obtener_por_id(id_grupo)
        self.estudiantes = self.grupo.estudiantes.all()
        self.calificaciones_cualitativas = CalificacionCualitativa.obtener_activos()
        self.preguntas = self.actividad.preguntas_asociadas.all()

        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.actividad.tipo_calificacion=='Cuantitativa':
            return NotaEstudianteCuantitativoForm
        return NotaEstudianteCualitativoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['estudiantes'] = self.estudiantes
        context['preguntas'] = self.preguntas
        context['actividad'] = self.actividad
        context['grupo'] = self.grupo
        context['calificaciones_cualitativas'] = self.calificaciones_cualitativas

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['estudiantes'] = self.estudiantes
        kwargs['preguntas'] = self.preguntas

        return kwargs

    def get_initial(self):
        initial = super().get_initial()

        for estudiante in self.estudiantes:
            for pregunta in self.preguntas:
                if Nota.existe_por_estudiante_y_pregunta(estudiante.pk, pregunta.pk) is True:

                    if self.actividad.tipo_calificacion=='Cuantitativa':
                        initial[f'{estudiante.pk}-{pregunta.pk}'] = Nota.obtener_por_estudiante_y_pregunta(estudiante.pk, pregunta.pk).resultado
                    else:
                        initial[f'{estudiante.pk}-{pregunta.pk}'] = Nota.obtener_por_estudiante_y_pregunta(estudiante.pk, pregunta.pk).calificacion_cualitativa

        return initial

    def form_valid(self, form):
        try:
            calificacion_por_estudiante = dict(self.request.POST)
            calificacion_por_estudiante.pop('DataTables_Table_0_length')
            calificacion_por_estudiante.pop('csrfmiddlewaretoken')

            ids_estudiantes = list(self.estudiantes.values_list('pk', flat=True))
            ids_preguntas = list(self.preguntas.values_list('pk', flat=True))
            ids_calificaciones_cualitativas = list(self.calificaciones_cualitativas.values_list('pk', flat=True))

            print(calificacion_por_estudiante)
            for estudiante_pregunta, calificaciones in calificacion_por_estudiante.items():
                estudiante = int(estudiante_pregunta.split('-')[0])
                pregunta = int(estudiante_pregunta.split('-')[1])
                calificacion = int(calificaciones[0])

                resultado = 0.0
                calificacion_cualitativa = None

                print(f'{estudiante} -- {pregunta} --> {calificacion}')

                if estudiante not in ids_estudiantes or pregunta not in ids_preguntas:
                    # Error al asociar las preguntas, hay preguntas que no pertenecen a la actividad
                    return self.form_invalid()

                if self.actividad.tipo_calificacion=='Cualitativa' and calificacion not in ids_calificaciones_cualitativas:
                    # Error al asociar las respuestas, hay respuestas que no pertenecen las  predeterminadas
                    return self.form_invalid()

                if self.actividad.tipo_calificacion=='Cuantitativa' and (calificacion<0 or calificacion>5):
                    # Error al asociar las respuestas, hay valores que están fuera del rango(0.0 - 5.0)
                    return self.form_invalid()

                if self.actividad.tipo_calificacion=='Cualitativa':
                    calificacion_cualitativa = CalificacionCualitativa.obtener_por_id(calificacion)
                else:
                    resultado = calificacion


                if Nota.existe_por_estudiante_y_pregunta(estudiante, pregunta) is True:
                    nota = Nota.obtener_por_estudiante_y_pregunta(estudiante, pregunta)
                    nota.resultado = resultado
                    nota.calificacion_cualitativa = calificacion_cualitativa
                    nota.save()
                else:
                    Nota.objects.create(
                        calificacion_cualitativa = calificacion_cualitativa,
                        pregunta = Pregunta.obtener_por_id(pregunta),
                        estudiante = Usuario.obtener_por_id(estudiante),
                        resultado = resultado
                    )
            messages.success(self.request, "Calificaciones registradas correctamente")

            return HttpResponseRedirect(self.request.path_info)

        except:
            messages.error(self.request, "Ha ocurrido un error al registrar las calificaciones")
        finally:
            return HttpResponseRedirect(self.request.path_info)



def generar_excel_calificaciones(request, id_grupo: int , id_actividad: int):
    import pandas as pd

    grupo = Grupo.obtener_por_id(id_grupo)
    actividad = Actividad.obtener_por_id(id_actividad)

    preguntas = list(actividad.preguntas_asociadas.all().values_list('contenido', flat=True))
    estudiantes = list(grupo.estudiantes.all().values_list('username', flat=True))

    data_frame = pd.DataFrame(index=estudiantes, columns=preguntas)

    print(data_frame.to_html())
