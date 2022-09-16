from django import template
from apps.competencias.models import ProfesorCursoPrograma

from apps.cursos.models import Curso, CursoDelPrograma

register = template.Library()

@register.simple_tag
def obtener_cursos_por_estudiante_y_periodo_academico(id_estudiante: int, id_periodo_academico: int):
    return Curso.obtener_cursos_por_estudiante_y_periodo_academico(id_estudiante, id_periodo_academico)

@register.simple_tag
def obtener_por_curso_programa_id(id_curso: int, id_programa: int):
    return CursoDelPrograma.obtener_por_curso_programa_id(id_curso, id_programa)

@register.simple_tag
def obtener_por_curso_programa_y_periodo_academico(id_curso_del_programa: int, id_periodo_academico: int):
    return ProfesorCursoPrograma.obtener_por_curso_programa_y_periodo_academico(id_curso_del_programa, id_periodo_academico)