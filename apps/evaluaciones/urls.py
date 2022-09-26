from django.urls import path

from apps.evaluaciones.views import (CalificarEvaluacionesEstudiantes,
                                    ListadoEvaluacionesProfesorCursoPrograma,
                                    SubirArchivoCalificacionesForm,
                                    generar_excel_calificaciones)


app_name = "evaluaciones"
urlpatterns = [
    path('listado-actividades-por-profesor-curso-programa/<int:id_profesor_curso_programa>/<int:id_grupo>',
        ListadoEvaluacionesProfesorCursoPrograma.as_view(),
        name='listado_actividades_por_profesor_curso_programa'
    ),
    path("calificar-evaluaciones/<int:id_grupo>/<int:id_actividad>", CalificarEvaluacionesEstudiantes.as_view(), name='calificar_evaluaciones'),

    path("generar-excel/<int:id_grupo>/<int:id_actividad>", generar_excel_calificaciones, name="generar_excel"),

    path("subir-calificaciones/<int:id_grupo>/<int:id_actividad>", SubirArchivoCalificacionesForm.as_view(), name="subir_calificaciones")
]