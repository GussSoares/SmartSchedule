from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from ..cliente.models import Cliente


@login_required
def index(request):
    active_clients = Cliente.objects.filter(is_active=True).count()

    context = {
        'user': request.user,
        'active_clients': active_clients
    }
    return render(request, 'dashboard/index.html', context)
