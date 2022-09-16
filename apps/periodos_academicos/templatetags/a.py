from django import template


register = template.Library()

@register.simple_tag
def obtener_niveles(curso) -> list:
    return curso.obtener_niveles_evaluacion_cursos()