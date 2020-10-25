from django.contrib import messages
from django.shortcuts import render

from .models import Location
from ..cliente.models import Coordinator


def create(request):
    if request.user.is_coordinator:
        grupo = Coordinator.objects.get(cliente=request.user).grupo
        if not Location.objects.filter(grupo=grupo).exclude(active=False):
            messages.warning(request, "Atenção! Você precisa ativar alguma localização para confirmação da presença das escalas!", extra_tags="warning alert-always")
    return render(request, 'location/list.html')
