from django.urls import path

from apps.competencias.views import ListadoGruposProfesorCursoPrograma



app_name="competencias"

urlpatterns = [
    path('listado-grupos-por-profesor-curso-programa/<int:id_profesor_curso_programa>',
         ListadoGruposProfesorCursoPrograma.as_view(),
         name='listado_grupos_por_profesor_curso_programa'
    ),

]