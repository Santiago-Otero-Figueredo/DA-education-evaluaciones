from django.db import models
from django.db.models import QuerySet
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.core.models import ModeloBase
from apps.usuarios.models import Usuario

from apps.cursos.models import CursoDelPrograma
from apps.periodos_academicos.models import PeriodoAcademico

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from apps.cursos.models import Curso

class TipoNivelEvaluacion(ModeloBase):
    tipo_superior = models.ForeignKey(
        'self',
        verbose_name='Tipo de nivel superior',
        related_name='sub_niveles_evaluacion',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    nombre = models.CharField(max_length=255, verbose_name="Nombre tipo de nivel")
    descripcion = models.TextField(verbose_name="Descripción del tipo de nivel")
    nivel = models.PositiveIntegerField(verbose_name="Nivel de jerarquía de las evaluaciones")
    mide_programa = models.BooleanField(default=False, verbose_name="Determina si este tipo de niveles son para medir programas")

    class Meta:
        ordering = ['nivel']

    def __str__(self):
        return self.nombre

    @staticmethod
    def obtener_ultimo_tipo():
        return TipoNivelEvaluacion.objects.order_by('nivel').last()


class NivelEvaluacion(ModeloBase):
    tipo_nivel = models.ForeignKey(
        TipoNivelEvaluacion,
        verbose_name="Tipo nivel evaluación",
        related_name="niveles_evaluacion_asociados",
        on_delete=models.PROTECT
    )
    curso_del_programa = models.ForeignKey(
        CursoDelPrograma,
        verbose_name="Curso del programa",
        related_name="niveles_evaluacion_asociados",
        on_delete=models.PROTECT
    )
    nivel_asociado = models.ForeignKey(
        'self',
        verbose_name="Nivel padre",
        related_name="sub_niveles_evaluacion",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    metas_curso_del_programa = models.ManyToManyField(
        CursoDelPrograma,
        verbose_name="Curso del programa asociados a metas en este novel de evaluación",
        through='competencias.MetaObjetivo',
        related_name="metas_niveles_evaluacion_asociados",
    )
    nombre = models.CharField(max_length=255, verbose_name="Nombre de nivel de evaluación")
    descripcion = models.TextField(verbose_name="Descripción nivel evaluación")
    mide_porcentaje = models.BooleanField(
        default=False,
        verbose_name="Determina si este tipo de nivel mide un porcentaje a cumplir por los niveles evaluación asociados"
    )
    porcentaje = models.FloatField(
        default=0.0,
        verbose_name="Porcentaje a cumplir por la sumatoria de los niveles evaluación asociados",
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    class Meta:
        ordering = ['tipo_nivel', 'nombre']

    def __str__(self) -> str:
        return f'{self.tipo_nivel} - {self.nombre}'

    @staticmethod
    def obtener_niveles_evaluacion_por_lista_ids_cursos(lista_ids: List[int]) -> QuerySet['NivelEvaluacion']:
        return NivelEvaluacion.objects.filter(
            curso_del_programa__curso__pk__in=lista_ids
        )

    @staticmethod
    def obtener_nivel_evaluacion_por_curso(id_curso: int) -> Optional['NivelEvaluacion']:
        try:
            return NivelEvaluacion.objects.filter(curso_del_programa__curso__pk=id_curso)
        except:
            return None

    @staticmethod
    def obtener_nivel_evaluacion_por_curso_del_programa_periodo_profesor(id_curso_programa: int, id_periodo_academico: int, id_profesor: int) -> Optional['NivelEvaluacion']:

        return NivelEvaluacion.objects.filter(
            curso_del_programa__pk=id_curso_programa,
            curso_del_programa__profesor_curso_programa_asociados__periodo_academico__pk=id_periodo_academico,
            curso_del_programa__profesor_curso_programa_asociados__profesor__pk=id_profesor
        )

    @staticmethod
    def obtener_por_curso_del_programa_y_periodo_academico(id_curso_programa: int, id_periodo_academico: int) -> Optional['NivelEvaluacion']:
        return NivelEvaluacion.objects.filter(
            curso_del_programa__pk=id_curso_programa,
            curso_del_programa__profesor_curso_programa_asociados__periodo_academico__pk=id_periodo_academico
        )



    def obtener_porcentaje_preguntas(self, id_profesor_curso_programa: int) -> float:
        porcentajes = list(self.restricciones_nivel_evaluacion_asociados.filter(
            profesor_curso_programa__pk=id_profesor_curso_programa
        ).values_list('porcentaje', flat=True))
        print(porcentajes)
        return sum(porcentajes)

    def obtener_porcentajes_subniveles(self):
        sub_niveles = self.sub_niveles_evaluacion.all()
        porcentaje_total = 0.0
        for sub_nivel in sub_niveles:
            porcentaje_total += sub_nivel.obtener_porcentaje_preguntas()
        return porcentaje_total

    def obtener_descripcion_completa(self):
        return f'{self.nombre} - {self.descripcion}'


class MetaObjetivo(ModeloBase):
    nivel_evaluacion = models.ForeignKey(
        NivelEvaluacion,
        verbose_name="Nivel de evaluacion asociado las metas de un curso del programa",
        related_name="metas_ascociadas",
        on_delete=models.PROTECT,
    )
    curso_del_programa = models.ForeignKey(
        CursoDelPrograma,
        verbose_name="Curso del programa asociado las metas de un nivel de evaluación",
        related_name="metas_ascociadas",
        on_delete=models.PROTECT,
    )
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la meta")
    valor = models.FloatField(
        verbose_name="Valor objetivo a cumplir para un nivel de evaluacion en un curso del programa",
        validators=[MinValueValidator(0.0)]
    )

    class Meta:
        ordering = ['nivel_evaluacion', 'curso_del_programa', 'nombre', 'valor']

    def __str__(self):
        return f'{self.nivel_evaluacion} - {self.curso_del_programa} - {self.nombre} - {self.valor}'


class ProfesorCursoPrograma(ModeloBase):
    curso_programa = models.ForeignKey(
        CursoDelPrograma,
        verbose_name="Curso del programa",
        related_name="profesor_curso_programa_asociados",
        on_delete=models.PROTECT
    )
    periodo_academico = models.ForeignKey(
        PeriodoAcademico,
        verbose_name="Periodo académico",
        related_name="profesor_curso_programa_asociados",
        on_delete=models.PROTECT
    )
    profesor = models.ForeignKey(
        Usuario,
        verbose_name="Profesor",
        related_name="profesor_curso_programa_asociados",
        on_delete=models.PROTECT
    )
    niveles_evaluacion = models.ManyToManyField(
        NivelEvaluacion,
        verbose_name="Niveles de evaluación asociados",
        related_name="profesor_curso_programa_asociado_a_niveles_evaluacion",
        through='competencias.RestriccionNivelProfesorCurso'
    )
    estudiantes_asignados = models.ManyToManyField(
        Usuario,
        verbose_name="Estudiantes asignados a este profesor de un curso del programa",
        related_name="profesor_curso_programa_asociados_a_estudiante",
        through='competencias.Grupo'
    )

    class Meta:
        ordering = ['periodo_academico', 'curso_programa', 'profesor']

    def __str__(self):
        return f'{self.periodo_academico} - {self.curso_programa} - {self.profesor}'

    @staticmethod
    def obtener_por_curso_del_programa_profesor_y_periodo_academico(
            id_curso_del_programa: int,
            id_profesor: int,
            id_periodo_academico: int
        ) -> Optional['ProfesorCursoPrograma']:

        try:
            return ProfesorCursoPrograma.objects.get(
                curso_programa__pk=id_curso_del_programa,
                profesor__pk = id_profesor,
                periodo_academico = id_periodo_academico
            )
        except:
            return None


    @staticmethod
    def obtener_por_curso_programa_y_periodo_academico(
            id_curso_del_programa: int,
            id_periodo_academico: int
        ) -> Optional['ProfesorCursoPrograma']:

        try:
            return ProfesorCursoPrograma.objects.get(
                curso_programa__pk=id_curso_del_programa,
                periodo_academico = id_periodo_academico
            )
        except:
            return None


class Grupo(ModeloBase):
    profesor_curso_programa = models.ForeignKey(
        ProfesorCursoPrograma,
        verbose_name="Profesor de un curso de programa",
        related_name="grupos_asociados",
        on_delete=models.PROTECT
    )
    estudiante = models.ForeignKey(
        Usuario,
        verbose_name="Estudiante de un curso de programa",
        related_name="grupos_asociados",
        on_delete=models.PROTECT
    )
    nombre = models.CharField(max_length=50, verbose_name="Nombre del grupo")
    fecha_creacion = models.DateTimeField(editable=False, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['profesor_curso_programa', 'nombre', 'fecha_creacion']

    def __str__(self):
        return f'{self.profesor_curso_programa} - {self.nombre}'


class RestriccionNivelProfesorCurso(ModeloBase):
    profesor_curso_programa = models.ForeignKey(
        ProfesorCursoPrograma,
        verbose_name="Profesor del curso del programa",
        related_name="restricciones_nivel_evaluacion_asociados",
        on_delete=models.PROTECT
    )
    nivel_evaluacion = models.ForeignKey(
        NivelEvaluacion,
        verbose_name="Nivel de evaluacion",
        related_name="restricciones_nivel_evaluacion_asociados",
        on_delete=models.PROTECT
    )
    porcentaje = models.FloatField(
        verbose_name="Porcentaje",
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    class Meta:
        ordering = ['nivel_evaluacion', 'profesor_curso_programa', 'porcentaje']

    def __str__(self):
        return f'{self.nivel_evaluacion} - {self.profesor_curso_programa} - {self.porcentaje}'