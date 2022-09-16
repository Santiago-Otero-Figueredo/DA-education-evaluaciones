from django.db import models
from django.db.models import QuerySet


from apps.core.models import ModeloBase
from apps.usuarios.models import Usuario


class Programa(ModeloBase):
    NIVELES_ACADEMICOS = (
        ("Pregrado", "Pregrado"),
        ("Maestría", "Maestría"),
        ("Doctorado", "Doctorado"),
    )
    nombre = models.CharField(max_length=200, verbose_name="nombre del programa")
    codigo = models.CharField(max_length=4, verbose_name="código del programa")
    nivel_academico = models.CharField(max_length=10, choices=NIVELES_ACADEMICOS, verbose_name="nivel académico")
    # similar a directores
    responsables = models.ManyToManyField(
        Usuario,
        related_name="programas_es_responsable",
        verbose_name="Seleccione los directores encargados de dirigir el programa académico"
    )

    class Meta:
        ordering = ("nombre",)
        permissions = (
            ("gestionar_programas", "Gestionar programas"),
        )

    def __str__(self):
        return self.nombre

    @staticmethod
    def obtener_programas_por_estudiante(estudiante_id: int) -> QuerySet['Programa']:

        programas_ids = set(Programa.objects.filter(
            cursos_del_programa__matriculas_del_cursoprograma__estudiante__pk=estudiante_id
        ).values_list('pk', flat=True))

        return Programa.obtener_por_lista_ids(programas_ids)