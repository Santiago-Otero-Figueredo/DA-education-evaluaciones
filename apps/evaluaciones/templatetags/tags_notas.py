from django import template

from apps.evaluaciones.models import Nota
from apps.usuarios.models import Usuario

register = template.Library()

@register.simple_tag
def obtener_notas_por_estudiante_y_actividad(id_estudiante: int, id_actividad: int):
    return Nota.obtener_varias_por_estudiante_y_actividad(id_estudiante, id_actividad)


@register.simple_tag
def transforma_lista_a_matrix(lista:list, filas: int, columnas: int):

    copia_lista = lista
    matrix = []
    while copia_lista != []:
        matrix.append(copia_lista[:columnas])
        copia_lista = copia_lista[columnas:]

    return matrix

@register.simple_tag
def obtener_id_estudiante(value: str):
    return value.split('-')[0]

@register.simple_tag
def obtener_estudiante(id_estudiante: int):
    return Usuario.obtener_por_id(id_estudiante)