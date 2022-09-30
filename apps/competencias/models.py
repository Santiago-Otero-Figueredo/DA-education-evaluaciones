from django.db import models
from django.db.models import QuerySet
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.core.models import ModeloBase
from apps.usuarios.models import Usuario

from apps.cursos.models import CursoDelPrograma
from apps.periodos_academicos.models import PeriodoAcademico

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from apps.evaluaciones.models import Actividad


def sumar_cantidad_hijos_hoja(informacion_hijos: List) -> int:

    return sum(d['cantidad_hijos_hoja'] for d in informacion_hijos)

class TipoNivelEvaluacion(ModeloBase):
    """
        Este modelo hace referencia a los tipos de niveles de evaluación que puede tener una institución educativa. Son las
        categorías en las que están agrupados los niveles de evaluación. Por ejemplo(Competencias, Resultados de aprendizaje,
        indicadores de logro, etc)

        Estos tipos están organizados de forma jerárquica, siendo el primer de todos aquel que tiene el atributo nivel = 1 y
        el tipo_superior = None
    """
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
        return f'{self.nombre}. {self.descripcion}'

    @staticmethod
    def obtener_ultimo_tipo():
        return TipoNivelEvaluacion.objects.order_by('nivel').last()


class NivelEvaluacion(ModeloBase):
    """
        Este modelo hace referencia a los niveles de evaluación según su categoría(TipoNivelEvaluacion) para una institución educativa.
        Son los aspectos que se quieren evaluar dentro del programa académico para un curso. Estos aspectos están agrupados por categorías
        y algunos definen los porcentajes que deben ser asignados para evaluar en el curso.

    """
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
    def obtener_por_curso_del_programa_y_periodo_academico(id_curso_programa: int, id_periodo_academico: int) -> QuerySet['NivelEvaluacion']:
        return NivelEvaluacion.objects.filter(
            curso_del_programa__pk=id_curso_programa,
            curso_del_programa__profesor_curso_programa_asociados__periodo_academico__pk=id_periodo_academico
        )


    @staticmethod
    def obtener_informacion_niveles_raiz_formato_json(id_curso_programa: int, id_periodo_academico: int) -> dict:
        niveles_evaluacion = NivelEvaluacion.objects.filter(
            nivel_asociado__isnull=True,
            curso_del_programa__pk=id_curso_programa,
            curso_del_programa__profesor_curso_programa_asociados__periodo_academico__pk=id_periodo_academico
        )

        listado_niveles = []
        for index, nivel_evaluacion in enumerate(niveles_evaluacion):
            informacion_hijos = nivel_evaluacion.obtener_informacion_niveles_hijos_formato_json()
            listado_niveles.append(
                {
                    'es_primer_elemento': (index==0),
                    'es_elemento_raiz': True,
                    'nombre': nivel_evaluacion.nombre,
                    'descripcion': nivel_evaluacion.descripcion,
                    'mide_porcentaje': nivel_evaluacion.mide_porcentaje,
                    'porcentaje': nivel_evaluacion.porcentaje,
                    'cantidad_hijos_hoja': sumar_cantidad_hijos_hoja(informacion_hijos),
                    'informacion_hijos': informacion_hijos
                }
            )


        return listado_niveles



    def obtener_informacion_niveles_hijos_formato_json(self) -> dict:

        niveles_hijos = self.sub_niveles_evaluacion.all()

        listado_niveles = []
        for index, nivel_evaluacion in enumerate(niveles_hijos):
            listado_niveles.append(
                {
                    'es_primer_elemento': (index==0),
                    'es_elemento_raiz': False,
                    'nombre': nivel_evaluacion.nombre,
                    'descripcion': nivel_evaluacion.descripcion,
                    'mide_porcentaje': nivel_evaluacion.mide_porcentaje,
                    'porcentaje': nivel_evaluacion.porcentaje,
                    'cantidad_hijos_hoja': len(nivel_evaluacion.obtener_informacion_niveles_hijos_formato_json()),
                    'informacion_hijos': nivel_evaluacion.obtener_informacion_niveles_hijos_formato_json(),
                    'pk': nivel_evaluacion.pk
                }
            )


        return listado_niveles


    def obtener_cantidad_total_hijos_hoja(self, cantidad=0) -> dict:


        if self.sub_niveles_evaluacion.all().count() == 0:
            return  0
        else:
            #cantidad += self.sub_niveles_evaluacion.all().count()
            for nivel in self.sub_niveles_evaluacion.all():
                cantidad += nivel.sub_niveles_evaluacion.all().count()
                nivel.obtener_cantidad_total_hijos_hoja(cantidad)

            return cantidad









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
    """
        Este modelo hace referencia al profesor de un curso de programa para un periodo academico.
        por ejemplo, El profesor Jose dicta el curso de bases de datos para el programa de ingeniería informática
        en el semestre II del año 2022

        Esta asociado al modelo estudiantes mediante el modelo Grupo del modulo competencias
        Esta asociado al modelo RestriccionNivelProfesorCurso del modulo competencias
        Esta asociado al modelo Actividad del modulo evaluaciones
    """
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

    def obtener_actividades(self) -> QuerySet['Actividad']:
        return self.actividades_asociadas.all()


class Grupo(ModeloBase):
    """
        Este modelo hacer referencia  ala relación entre un estudiante y un profesor de un curso de programa en un periodo academico.
        por ejemplo, el estudiante Santiago esta asociado al profesor Jose que dicta el curso de bases de datos para el programa de ingeniería informática
        en el semestre II del año 2022 en el grupo C
    """
    profesor_curso_programa = models.ForeignKey(
        ProfesorCursoPrograma,
        verbose_name="Profesor de un curso de programa",
        related_name="grupos_asociados",
        on_delete=models.PROTECT
    )
    estudiantes = models.ManyToManyField(
        Usuario,
        verbose_name="Estudiante de un curso de programa",
        related_name="grupos_asociados"
    )
    nombre = models.CharField(max_length=50, verbose_name="Nombre del grupo")

    class Meta:
        ordering = ['profesor_curso_programa', 'nombre']

    def __str__(self):
        return f'{self.profesor_curso_programa} - {self.nombre}'

    @staticmethod
    def obtener_grupos_de_profesor_curso_programa(id_profesor_curso_programa: int) -> QuerySet['Grupo']:
        profesor_curso_programa = ProfesorCursoPrograma.obtener_por_id(id_profesor_curso_programa)
        return profesor_curso_programa.grupos_asociados.all()

    def obtener_estudiantes(self) -> QuerySet['Usuario']:

        return Usuario.objects.filter(
            grupos_asociados__pk=self.pk
        )


class RestriccionNivelProfesorCurso(ModeloBase):
    """
        Este modelo hace referencia al porcentaje que debe tener un nivel de evaluacion al ser evaluado por un profesor, este valor es definido
        libremente por el profesor, la única condición que se debe cumplir es que la suma de porcentajes para todos los registros de este profesor
        en un curso de un programa en un periodo academico no supere el limite del nivel de evaluacion superior del nivel de evalaución actual.
        por ejemplo, para el nivel de evaluacion I.L.1 Visualiza adecuadamente señales periódicas y transitorias en un osciloscopio

    """
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
