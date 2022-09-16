from django.urls import path

from apps.dashboards.views import (CursosEvaluacion,
                                    ResumenNivelesEvaluacion,
                                    ResumenNivelesEvaluacionPorProfesor,
                                    ResumenCalificaciones,
                                    ResumenCalificacionesPorEvaluacion,

                                    CursosPorEstudiante,

                                    Inicio)

app_name = "dashboards"
urlpatterns = [
    path("inicio/", Inicio.as_view(), name='inicio'),

    path("evaluacion-cursos/", CursosEvaluacion.as_view(), name="evaluacion_cursos"),
    path("resumen-niveles-evaluacion/<int:id_curso>/<int:id_periodo_academico>", ResumenNivelesEvaluacionPorProfesor.as_view(), name="niveles_evaluacion"),
    path("resumen-calificaciones/<int:id_estudiante>/<int:id_profesor_curso_programa>", ResumenCalificaciones.as_view(), name="resumen_calificaciones"),
    path("resumen-calificaciones-por-evaluacion/<int:id_estudiante>/<int:id_profesor_curso_programa>", ResumenCalificacionesPorEvaluacion.as_view(), name="resumen_calificaciones_por_evaluacion"),

    path("cursos-estudiante/<int:id_estudiante>", CursosPorEstudiante.as_view(), name="cursos_estudiante"),

]