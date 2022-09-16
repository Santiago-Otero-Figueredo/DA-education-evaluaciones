from django.db import models
from django.db.models import QuerySet

from typing import List, Set
from apps.core.models import ModeloBase


class PeriodoAcademico(ModeloBase):
    PERIODO_UNO = "I"
    PERIODO_DOS = "II"
    PERIODO_TRES = "III"
    PERIODOS = (
        (PERIODO_UNO, "I"),
        (PERIODO_DOS, "II"),
        (PERIODO_TRES, "III"),
    )
    ano = models.PositiveIntegerField(verbose_name="año del periodo académico")
    periodo = models.CharField(max_length=3, choices=PERIODOS, verbose_name="periodo académico")

    fecha_inicio = models.DateField(verbose_name="fecha de inicio del periodo académico")
    fecha_fin = models.DateField(verbose_name="fecha de finalización del periodo académico")


    class Meta:
        ordering = ["-ano", "-periodo"]
        unique_together = (("ano", "periodo",),)
        permissions = (
            ("gestionar_periodos_academicos", "Periodos académicos - Gestionar"),
        )

    def __str__(self):
        return "{}-{}".format(self.ano, self.periodo)

    @staticmethod
    def obtener_periodos_academicos_por_ano(ano: int) -> QuerySet['PeriodoAcademico']:
        return PeriodoAcademico.obtener_activos().filter(ano=ano).order_by('periodo')

    @staticmethod
    def obtener_periodos_academicos_por_ano_y_lista_ids(ano: int, lista_ids: List[int]) -> QuerySet['PeriodoAcademico']:
        return PeriodoAcademico.obtener_por_lista_ids(lista_ids).filter(ano=ano).order_by('periodo')

    @staticmethod
    def obtener_anos() -> Set[int]:
        return set(PeriodoAcademico.obtener_activos().values_list('ano', flat=True))

    def obtener_cursos_por_periodo_academico(self) -> dict:
        from apps.cursos.models import Curso

        return Curso.obtener_activos().filter(
            programas_del_curso__matriculas_del_cursoprograma__periodo_academico__pk=self.pk
        ).distinct('nombre')

