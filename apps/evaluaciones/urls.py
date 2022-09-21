from django.urls import path

from apps.evaluaciones.views import CalificarEvaluacionesEstudiantes, EstudiantesPorEvaluacion, ListadoEvaluacionesProfesorCursoPrograma


app_name = "evaluaciones"
urlpatterns = [
    path('listado-actividades-por-profesor-curso-programa/<int:id_profesor_curso_programa>/<int:id_grupo>',
        ListadoEvaluacionesProfesorCursoPrograma.as_view(),
        name='listado_actividades_por_profesor_curso_programa'
    ),
    path("estudiantes-evaluacion/<int:id_profesor_curso_programa>/<int:id_grupo>/<int:id_actividad>", EstudiantesPorEvaluacion.as_view(), name='estudiantes_evaluacion'),
    path("calificar-evaluaciones/<int:id_grupo>/<int:id_actividad>/<int:id_estudiante>", CalificarEvaluacionesEstudiantes.as_view(), name='calificar_evaluaciones'),
]