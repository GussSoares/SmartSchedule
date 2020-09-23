from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..escala.forms import CreateScheduleForm


@login_required
def create(request):
    form = CreateScheduleForm()
    context = {
        'form': form
    }
    return render(request, 'escala/create.html', context)
