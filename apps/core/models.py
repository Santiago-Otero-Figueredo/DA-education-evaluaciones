from django.db import models

from django.db.models import QuerySet
from typing import Optional, List


class ModeloBase(models.Model):
    #fecha_creacion = models.DateTimeField(editable=False, auto_now_add=True)
    #fecha_modificacion = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=True)


    class Meta:
        abstract = True


    @classmethod
    def obtener_todos(cls) -> QuerySet['ModeloBase']:
        return cls.objects.all()

    @classmethod
    def obtener_activos(cls) -> QuerySet['ModeloBase']:
        return cls.objects.filter(activa=True)

    @classmethod
    def obtener_por_id(cls, id: int) -> Optional['ModeloBase']:

        try:
            return cls.objects.get(pk=id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def obtener_por_lista_ids(cls, lista_ids: List[int]) -> QuerySet['ModeloBase']:

        return cls.objects.filter(pk__in=lista_ids)


