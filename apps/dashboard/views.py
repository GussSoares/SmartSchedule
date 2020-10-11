from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from ..cliente.models import Client, Member, Coordinator, Group
from ..escala.models import Schedule
from ..notification.models import Commentary
from ..core.utils import timezone, today
import datetime




@login_required
def index(request):

    if request.user.is_coordinator:
        group = Coordinator.objects.get(cliente=request.user).grupo
        # membros adicionados nos ultimos 15 dias
        active_members = Member.objects.filter(cliente__is_active=True, grupo=group).count()
        last_members = Member.objects.filter(cliente__created_at__gte=today()-datetime.timedelta(days=15), grupo=group).order_by('-cliente__created_at')
        schedules = Schedule.objects.filter(schedulemember__membro__grupo=group).distinct().count()
        groups = []
    elif request.user.is_superuser:
        active_members = Member.objects.filter(cliente__is_active=True).count()
        last_members = Member.objects.filter(cliente__created_at__gte=(today()-datetime.timedelta(days=15))).order_by('-cliente__created_at')
        schedules = Schedule.objects.all().count()
        groups = Group.objects.all().count()
        # comentarios dos ultimos 15 dias
    else:
        last_members = []
        schedules = []
        active_members = []
        groups = []

    context = {
        'user': request.user,
        'active_members': active_members,
        'last_members': last_members,
        'schedules': schedules,
        'groups': groups
    }
    return render(request, 'dashboard/index.html', context)
