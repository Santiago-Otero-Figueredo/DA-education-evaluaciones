from apps.evaluaciones.models import Nota, Pregunta, CalificacionCualitativa
from apps.usuarios.models import Usuario



def cargar_calificaciones(elemento, actividad):
    pregunta_contenido = elemento.name
    pregunta = actividad.obtener_actividad_por_contenido(pregunta_contenido)
    calificaciones_por_estudiante = elemento.to_dict()
    print("ACTIVIDAD: ", actividad)
    print(actividad.tipo_calificacion)
    for codigo_estudiante, calificacion in calificaciones_por_estudiante.items():

        calificacion_cualitativa = None
        estudiante = Usuario.obtener_estudiante_por_codigo(str(codigo_estudiante))

        if actividad.tipo_calificacion == 'Cualitativa':
            calificacion_cualitativa = CalificacionCualitativa.obtener_calificacion_por_numero(calificacion)
            calificacion = 0.0
            print(calificacion_cualitativa)

        if Nota.existe_por_estudiante_y_pregunta(estudiante.pk, pregunta.pk) is True:
            nota = Nota.obtener_por_estudiante_y_pregunta(estudiante.pk, pregunta.pk)
            nota.resultado = calificacion
            nota.calificacion_cualitativa = calificacion_cualitativa
            nota.save()
        else:
            Nota.objects.create(
                calificacion_cualitativa = calificacion_cualitativa,
                pregunta = pregunta,
                estudiante = estudiante,
                resultado = calificacion
            )
