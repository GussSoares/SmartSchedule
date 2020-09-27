from django.db import models
from apps.core.models import DefaultModel

NOTIFICATION_STATUS = [('pending', 'Pendente'), ('sent', 'Envidado'), ('error', 'Erro')]


class Notification(DefaultModel):
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, choices=NOTIFICATION_STATUS)
    cliente = models.ForeignKey('cliente.Client', null=True, blank=True, on_delete=models.SET_NULL)
    player_id = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'notificacao'
