from django.shortcuts import render
from ..escala.forms import CreateScheduleForm


def create(request):
    form = CreateScheduleForm()
    context = {
        'form': form
    }
    return render(request, 'escala/create.html', context)
