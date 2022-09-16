from django import template

from apps.competencias.models import NivelEvaluacion


register = template.Library()

@register.simple_tag
def obtener_porcentajes_curso_programa(id_nivel_evaluacion: int, id_profesor_curso_programa: int) -> list:
    return NivelEvaluacion.obtener_por_id(id_nivel_evaluacion).obtener_porcentaje_preguntas(id_profesor_curso_programa)