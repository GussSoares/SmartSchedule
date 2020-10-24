from django.db import models
from ..core.models import DefaultModel


class Location(DefaultModel):
    latitude = models.FloatField("Latitude")
    longitude = models.FloatField("Longitude")
    descricao = models.CharField("Descrição", max_length=255, null=False, default="Ponto")
    grupo = models.ForeignKey("cliente.Group", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'location'
