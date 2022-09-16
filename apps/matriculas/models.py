from django.db import models
from django.db.models import QuerySet

from typing import Optional, List

from apps.core.models import ModeloBase
from apps.cursos.models import CursoDelPrograma
from apps.usuarios.models import Usuario
from apps.periodos_academicos.models import PeriodoAcademico

class Matricula(ModeloBase):
    estudiante = models.ForeignKey(Usuario, related_name="matriculas_del_estudiante", on_delete=models.PROTECT)
    curso_del_programa = models.ForeignKey(CursoDelPrograma, related_name="matriculas_del_cursoprograma", on_delete=models.PROTECT)
    periodo_academico = models.ForeignKey(PeriodoAcademico, on_delete=models.PROTECT)
    # indica si termino el proceso de TG
    aprobada = models.BooleanField(null=True)
    # indica si la matricula sigue activa o no

    class Meta:
        permissions = (
            ("gestionar_matriculas", "Matriculas - Gestionar"),
        )
        ordering = ['periodo_academico']
