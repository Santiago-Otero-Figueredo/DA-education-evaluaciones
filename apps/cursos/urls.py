from django.urls import path

from apps.cursos.views import CursosAsigandosActualmente


app_name = "cursos"
urlpatterns = [
    path("cursos-asignados-profesor/<int:id_profesor>", CursosAsigandosActualmente.as_view(), name='cursos_asignados_profesor'),
]