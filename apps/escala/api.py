from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# from django.utils import timezone
from .models import Schedule, ScheduleMember
from ..cliente.models import Member
import datetime
import pytz

timezone = pytz.timezone(settings.TIME_ZONE)


@csrf_exempt
def create_schedule(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                schedule = Schedule(
                    inicio=timezone.localize(datetime.datetime.strptime(request.POST.get('start_date'), "%d/%m/%Y %H:%M:%S")),
                    fim=timezone.localize(datetime.datetime.strptime(request.POST.get('end_date'), "%d/%m/%Y %H:%M:%S")),
                    descricao=request.POST.get('text')
                )
                schedule.save()

                members_list = request.POST.get('owner').split(',')
                schedules_members = []
                for m in members_list:
                    schedules_members.append(ScheduleMember(
                        escala=schedule,
                        membro=Member.objects.get(id=m)
                    ))
                ScheduleMember.objects.bulk_create(schedules_members)
        except Exception as exc:
            return JsonResponse({'msg': 'error: '+str(exc)}, status=500)
        return JsonResponse({'id': schedule.id}, status=200)
    return JsonResponse({'msg': 'Method Not Supported'}, status=501)


@csrf_exempt
def update_schedule(request, pk):
    if request.method == 'POST':
        schedule = get_object_or_404(Schedule, pk=pk)
        schedule_members = schedule.schedulemember_set.all()
        try:
            with transaction.atomic():
                schedule.inicio = timezone.localize(datetime.datetime.strptime(request.POST.get('start_date'), "%d/%m/%Y %H:%M:%S"))
                schedule.fim = timezone.localize(datetime.datetime.strptime(request.POST.get('end_date'), "%d/%m/%Y %H:%M:%S"))
                schedule.descricao = request.POST.get('text')
                schedule.save()
                # remove os membros da escala
                schedule_members.delete()

                # coloca novamente os membros na escala
                members_list = request.POST.get('owner').split(',')
                schedules_members = []
                for m in members_list:
                    schedules_members.append(ScheduleMember(
                        escala=schedule,
                        membro=Member.objects.get(id=m)
                    ))
                ScheduleMember.objects.bulk_create(schedules_members)

        except Exception as exc:
            return JsonResponse({'msg': 'error: '+str(exc)}, status=500)
        return JsonResponse({'id': schedule.id}, status=200)
    return JsonResponse({'msg': 'Method Not Supported'}, status=501)


@csrf_exempt
def delete_schedule(request, pk):
    if request.method == 'POST':
        try:
            schedule = get_object_or_404(Schedule, pk=pk)
            schedule.delete()
        except Exception as exc:
            return JsonResponse({'msg': 'error: '+str(exc)}, status=200)
        return JsonResponse({'msg': 'success'}, status=200)
    return JsonResponse({'msg': 'Method Not Supported'}, status=501)


def get_all_schedules(request):
    schedules = Schedule.objects.all()
    result = []

    for schedule in schedules:
        result.append({
            'owner': list(schedule.schedulemember_set.all().values_list('membro_id', flat=True)),
            'start_date': schedule.inicio,
            'end_date': schedule.fim,
            'calendarId': '1',
            'category': 'time',
            'id': str(schedule.id),
            'text': schedule.descricao,
            'membros': list(schedule.schedulemember_set.all().values_list('membro__cliente__first_name', flat=True))
        })
    return JsonResponse({'data': result}, status=200)
