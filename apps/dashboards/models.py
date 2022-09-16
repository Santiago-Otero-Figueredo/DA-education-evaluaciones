from django.db import models
from django.db.models import Count, When, Case, IntegerField, FloatField, F, QuerySet

from typing import TYPE_CHECKING, List

from apps.cursos.models import Curso


if TYPE_CHECKING:
    from apps.periodos_academicos.models import PeriodoAcademico
    from apps.programas.models import Programa
# Create your models here.
class Reporte(models.Model):

    class Meta:
        managed = False

    @staticmethod
    def obtener_resumen_cursos_por_periodo_academico() -> dict:
        from apps.periodos_academicos.models import PeriodoAcademico

        return PeriodoAcademico.obtener_cursos_por_periodo_academico()

