from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.core.models import ModeloBase
from apps.usuarios.models import Usuario
from apps.competencias.models import RestriccionNivelProfesorCurso, NivelEvaluacion, ProfesorCursoPrograma
# Create your models here.

class TipoActividad(ModeloBase):
    restricciones_nivel_profesor_curso = models.ManyToManyField(
        'evaluaciones.RestriccionNivelActividad',
        verbose_name="Restricciones de nivel de evaluación para un profesor en un curso de programa",
        related_name="tipos_evaluacion_asociadas"
    )
    nombre = models.TextField(verbose_name="Nombre de la actividad de evaluación")

    class Meta:
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre

class RestriccionNivelActividad(ModeloBase):
    tipo_actividad = models.ForeignKey(
        TipoActividad,
        verbose_name="Actividad asociadas la evaluación y al profesor curso programa",
        related_name="restricciones_de_nivel_actividad_asociadas",
        on_delete=models.PROTECT
    )
    restriccion_nivel_profesor_curso = models.ForeignKey(
        RestriccionNivelProfesorCurso,
        verbose_name="Restricción de porcentaje para un profesor de un curso de programa y un nivel de evaluación",
        related_name="restricciones_de_nivel_actividad_asociadas",
        on_delete=models.PROTECT
    )
    porcentaje = models.FloatField(
        verbose_name='Porcentaje del tipo actividad con respecto a profesor curso del programa',
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    class Meta:
        ordering = ['tipo_actividad', 'restriccion_nivel_profesor_curso', 'porcentaje']

    def __str__(self) -> str:
        return f'{self.tipo_actividad} - {self.restriccion_nivel_profesor_curso} - {self.porcentaje}'


class Actividad(ModeloBase):
    TIPOS_CALIFICACIONES = (
        ('Cuantitativa', 'Cuantitativa'),
        ('Cualitativa', 'Cualitativa')
    )
    profesor_curso_programa = models.ForeignKey(
        ProfesorCursoPrograma,
        verbose_name="Profesor curso programa asociado",
        related_name="actividades_asociadas",
        on_delete=models.PROTECT
    )
    tipo_actividad = models.ForeignKey(
        TipoActividad,
        verbose_name="Tipo actividad asociadas",
        related_name="actividades_asociadas",
        on_delete=models.PROTECT
    )
    tipo_calificacion = models.CharField(
        max_length=12,
        verbose_name="El tipo de calificación (Cualitativa o Cuantitativa)",
        choices=TIPOS_CALIFICACIONES,
        default='Cualitativa'
    )
    nombre = models.TextField(verbose_name="Nombre de la evaluación")

    class Meta:
        ordering = ['profesor_curso_programa', 'tipo_actividad', 'nombre']

    def __str__(self) -> str:
        return f'{self.profesor_curso_programa} - {self.tipo_actividad} - {self.tipo_calificacion} - {self.nombre}'


class Pregunta(ModeloBase):
    actividad = models.ForeignKey(
        Actividad,
        verbose_name="Actividad asociada",
        related_name="preguntas_asociadas",
        on_delete=models.PROTECT
    )
    restriccion_nivel_actividad = models.ForeignKey(
        RestriccionNivelActividad,
        verbose_name="Restricción de porcentaje entre un tipo actividad y nivel evaluación para un profesor de un curso de un programa",
        related_name="preguntas_asociadas",
        on_delete=models.PROTECT
    )
    numeracion = models.PositiveIntegerField()
    contenido = models.CharField(max_length=255)
    porcentaje = models.FloatField(
        verbose_name='Porcentaje de la pregunta con respecto a la evaluación',
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    class Meta:
        ordering = ['numeracion', 'contenido', 'actividad', 'restriccion_nivel_actividad']

    def __str__(self) -> str:
        return f'{self.restriccion_nivel_actividad} - {self.actividad} - {self.numeracion}.{self.contenido} - {self.porcentaje}'


class CalificacionCualitativa(ModeloBase):
    nombre = models.CharField(max_length=25, verbose_name="Nombre que tiene esta calificación (Excelente, sobresaliente, etc)")
    valor_numerico = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name="Valor numérico asociado a esta calificación cuantitativa"
    )

    def __str__(self):
        return f'{self.valor_numerico} - {self.nombre}'

class Nota(ModeloBase):
    calificacion_cualitativa = models.ForeignKey(
        CalificacionCualitativa,
        verbose_name="Calificación cualitativa de la pregunta en la evaluación asociada",
        related_name="nota_de_estudiante_asociada",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    pregunta = models.ForeignKey(
        Pregunta,
        verbose_name="Pregunta de la evaluación asociada",
        related_name="nota_de_estudiante_asociada",
        on_delete=models.PROTECT
    )
    estudiante = models.ForeignKey(
        Usuario,
        verbose_name="Estudiante que respondió pregunta",
        related_name="nota_de_estudiante_asociada",
        on_delete=models.PROTECT
    )
    resultado = models.FloatField(
        verbose_name='Resultado cuantitativo de la respuesta',
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )


    def __str__(self) -> str:
        if self.calificacion_cualitativa:
            return f'{self.estudiante} - {self.pregunta} - {self.calificacion_cualitativa}'
        return f'{self.estudiante} - {self.pregunta} -  {self.resultado}'

    @staticmethod
    def obtener_por_estudiante_y_pregunta(id_estudiante: int, id_pregunta: int):
        try:
            return Nota.objects.get(estudiante__pk=id_estudiante, pregunta__pk=id_pregunta)
        except:
            return None

    @staticmethod
    def obtener_varias_por_estudiante_y_actividad(id_estudiante: int, id_actividad: int):
        return Nota.objects.filter(estudiante__pk=id_estudiante, pregunta__actividad__pk=id_actividad)


    @staticmethod
    def existe_por_estudiante_y_pregunta(id_estudiante: int, id_pregunta: int):
        return Nota.objects.filter(estudiante__pk=id_estudiante, pregunta__pk=id_pregunta).exists()


class CalificacionEvaluacion(ModeloBase):
    nivel_evaluacion = models.ForeignKey(
        NivelEvaluacion,
        verbose_name="Nivel de evaluación asociado al profesor curso programa",
        related_name="calificaciones_evaluacion_asociadas",
        on_delete=models.PROTECT
    )
    profesor_curso_programa = models.ForeignKey(
        RestriccionNivelProfesorCurso,
        verbose_name="Profesor curso programa asociado al nivel de evaluación",
        related_name="calificaciones_evaluacion_asociadas",
        on_delete=models.PROTECT
    )
    porcentaje = models.FloatField(
        verbose_name='Porcentaje del nivel evaluación con respecto al profesor curso programa',
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    class Meta:
        ordering = ['nivel_evaluacion', 'profesor_curso_programa', 'porcentaje']

    def __str__(self) -> str:
        return f'{self.nivel_evaluacion} - {self.profesor_curso_programa}. {self.porcentaje}'



