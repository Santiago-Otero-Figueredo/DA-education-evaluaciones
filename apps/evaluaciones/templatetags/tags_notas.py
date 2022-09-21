from django import template

from apps.evaluaciones.models import Nota

register = template.Library()

@register.simple_tag
def obtener_notas_por_estudiante_y_actividad(id_estudiante: int, id_actividad: int):
    return Nota.obtener_varias_por_estudiante_y_actividad(id_estudiante, id_actividad)
