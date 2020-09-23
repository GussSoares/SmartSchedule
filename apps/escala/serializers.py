from django.core import serializers
from ..cliente.models import Client
serializers.ModelSerializer()


serializers.serialize('json', Client.objects.all())
