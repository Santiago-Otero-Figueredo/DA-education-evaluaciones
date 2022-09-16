from django.shortcuts import render

from django.views.generic import ListView
# Create your views here.

from .models import Usuario

class ListadoEstudiantes(ListView):
    model = Usuario
    context_object_name = "usuarios"
    template_name = "usuarios/listado_estudiantes.html"

    def get_queryset(self):
        return Usuario.obtener_todos_los_estudiantes()