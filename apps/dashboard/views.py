from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from ..cliente.models import Client, Member
import datetime


@login_required
def index(request):
    today = datetime.date.today()
    active_clients = Client.objects.filter(is_active=True).count()
    last_members = Member.objects.filter(cliente__created_at__gte=today-datetime.timedelta(days=30)).order_by('-cliente__created_at')

    context = {
        'user': request.user,
        'active_clients': active_clients,
        'last_members': last_members
    }
    return render(request, 'dashboard/index.html', context)
