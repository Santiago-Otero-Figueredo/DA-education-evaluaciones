from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.views.generic import FormView, CreateView, ListView

from apps.evaluaciones.forms import NotaEstudianteCualitativoForm, NotaEstudianteCuantitativoForm, SubirArchivoForm

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


class SubirArchivoCalificacionesForm(FormView):
    form_class = SubirArchivoForm
    template_name = 'evaluaciones/subir_calificaciones.html'

    def dispatch(self, request, *args, **kwargs):
        id_actividad = self.kwargs.pop('id_actividad', 0)
        id_grupo = self.kwargs.pop('id_grupo', 0)

        self.actividad = Actividad.obtener_por_id(id_actividad)
        self.grupo = Grupo.obtener_por_id(id_grupo)
        self.estudiantes = self.grupo.estudiantes.all()
        self.calificaciones_cualitativas = CalificacionCualitativa.obtener_activos()
        self.preguntas = self.actividad.preguntas_asociadas.all()

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        kwargs = {
            'id_profesor_curso_programa':self.actividad.profesor_curso_programa.pk,
            'id_grupo':self.grupo.pk,
        }
        return reverse_lazy(
            'evaluaciones:listado_actividades_por_profesor_curso_programa',
            kwargs=kwargs
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['actividad'] = self.actividad
        context['grupo'] = self.grupo

        return context

    def form_valid(self, form):
        from apps.evaluaciones.utils import cargar_calificaciones
        import pandas as pd
        import numpy as np
        archivo = form.cleaned_data['archivo']

        calificaciones = pd.read_excel(
            archivo,
            index_col=[0, 1],
            engine='openpyxl'
        )


        preguntas_a_calificar = set(calificaciones.columns.to_list())
        estudiantes_a_calificar = set(calificaciones.index.values.tolist())

        estudiantes_en_el_grupo = set(self.estudiantes.values_list('codigo', flat=True))
        preguntas_en_la_actividad = set(self.preguntas.values_list('contenido', flat=True))

        calificaciones = calificaciones.fillna(0)

        if len(estudiantes_en_el_grupo.intersection(estudiantes_a_calificar)) > 0:
            messages.error(self.request, "Hay discrepancias entre los estudiantes del archivo y los estudiantes del grupo")
            return self.form_invalid(form)


        lista_preguntas_incluidas = []
        for a in preguntas_a_calificar:
            lista_preguntas_incluidas.append(a in preguntas_en_la_actividad)


        if all(lista_preguntas_incluidas) is False:
            messages.error(self.request, "Hay discrepancias entre las preguntas del archivo y las de la actividad")
            return self.form_invalid(form)

        try:
            calificaciones.astype(float)
        except Exception:
           messages.error(self.request, "Hay notas que no son números")
           return self.form_invalid(form)

        estado_calificaciones = calificaciones.gt(5.0)
        estado_calificaciones.astype(int)
        calificaciones_incorrectas = estado_calificaciones[estado_calificaciones > 0].stack().index.tolist()

        if len(calificaciones_incorrectas) > 0:
            messages.error(self.request, "Hay notas que están fuera de los rangos permitidos (0.0-5.0)")
            return self.form_invalid(form)

        calificaciones.reset_index(level='nombre_completo', inplace=True)
        calificaciones.drop('nombre_completo', axis=1, inplace=True)


        try:
            calificaciones.apply(cargar_calificaciones, actividad=self.actividad)
            messages.success(self.request, "Se cargaron las calificaciones correctamente")
            return super().form_valid(form)
        except Exception as e:
            print("ERROR: ", e)
            messages.error(self.request, "Se produjo un error al cargar las calificaciones")
            return self.form_invalid(form)


def generar_excel_calificaciones(request, id_grupo: int , id_actividad: int):
    from django.db.models import CharField, Value
    from django.db.models.functions import Concat
    import pandas as pd

    grupo = Grupo.obtener_por_id(id_grupo)
    actividad = Actividad.obtener_por_id(id_actividad)

    preguntas = list(actividad.preguntas_asociadas.all().values_list('contenido', flat=True))
    estudiantes = list(grupo.estudiantes.all().annotate(
        nombre_completo=Concat('first_name', Value(' '), 'last_name', output_field=CharField())
    ).values_list('codigo', 'nombre_completo'))

    index = pd.MultiIndex.from_tuples(estudiantes, names=["codigo", "nombre_completo"])
    data_frame = pd.DataFrame(index=index, columns=preguntas)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="G_{grupo.nombre}_A_{actividad.nombre}.xlsx"'
    data_frame.to_excel(response)
    return response
