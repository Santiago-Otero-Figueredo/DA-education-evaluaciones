from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from .views import *

app_name = "usuarios"

urlpatterns = [
    path('listado-estudiantes', ListadoEstudiantes.as_view(), name="listado_estudiantes"),
    path('listado-profesores', ListadoProfesores.as_view(), name="listado_profesores")
]