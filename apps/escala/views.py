from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..cliente.models import Coordinator
from ..escala.forms import CreateScheduleForm


@login_required
def create(request):
    if request.user.is_coordinator:
        grupo = Coordinator.objects.get(cliente=request.user).grupo
    else:
        grupo = None
    form = CreateScheduleForm(grupo=grupo)
    context = {
        'form': form
    }
    return render(request, 'escala/create.html', context)


def confirmar_presenca(request):
    return render(request, 'confirmar_presenca/confirmar_presenca.html')
