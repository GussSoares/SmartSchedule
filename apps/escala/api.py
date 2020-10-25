from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# from django.utils import timezone
from .models import Schedule, ScheduleMember
from ..cliente.models import Member, Coordinator
import datetime
import pytz
import json
from haversine import haversine, Unit
from ..core.utils import get_subdomain
from ..location.models import Location

timezone = pytz.timezone(settings.TIME_ZONE)


@csrf_exempt
def create_schedule(request):
    if request.method == 'POST':
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            with transaction.atomic(using=get_subdomain(request)):
                schedule = Schedule(
                    inicio=datetime.datetime.strptime(start, "%d/%m/%Y %H:%M:%S").astimezone(tz=timezone),
                    fim=datetime.datetime.strptime(end, "%d/%m/%Y %H:%M:%S").astimezone(tz=timezone),
                    descricao=request.POST.get('text'),
                    obs=request.POST.get('obs')
                )
                schedule.save()

                members_list = json.loads(request.POST.get('owner'))
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
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            with transaction.atomic(using=get_subdomain(request)):
                schedule.inicio = datetime.datetime.strptime(start, "%d/%m/%Y %H:%M:%S").astimezone(tz=timezone)
                schedule.fim = datetime.datetime.strptime(end, "%d/%m/%Y %H:%M:%S").astimezone(tz=timezone)
                schedule.descricao = request.POST.get('text')
                schedule.obs = request.POST.get('obs')

                schedule.save()
                # remove os membros da escala
                schedule_members.delete()

                # coloca novamente os membros na escala
                members_list = json.loads(request.POST.get('owner'))
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
    # todo: precisa pegar as escalas cujo usuario é coordenador d
    user = request.user

    if user.is_coordinator:
        group = Coordinator.objects.get(cliente=user).grupo
        schedules = Schedule.objects.filter(schedulemember__membro__grupo=group)
    elif user.is_member:
        member = Member.objects.get(cliente=user)
        schedules = Schedule.objects.filter(schedulemember__membro=member)
    else:
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
            'obs': schedule.obs,
            'membros': list(schedule.schedulemember_set.all().values_list('membro__cliente__first_name', flat=True))
        })
    return JsonResponse({'data': result}, status=200)


def get_member_by_schedule(request):
    pk = request.GET.get('dhx_crosslink_presence')
    if request.GET.get('uid', None):
        return JsonResponse([], safe=False, status=200)
    try:
        schedule = Schedule.objects.get(pk=pk)
    except Exception as exc:
        return JsonResponse([], safe=False, status=200)
    return JsonResponse([{"value": str(x.membro.id), "label": x.membro.cliente.first_name} for x in schedule.schedulemember_set.all()], safe=False, status=200)


def get_member_by_schedule_html_form(request):
    pk = request.GET.get('dhx_crosslink_presence')
    if request.GET.get('uid', None):
        return JsonResponse([], safe=False, status=200)
    try:
        schedule = Schedule.objects.get(pk=pk)
        html = """
        <div class="row">
            <div class="col-sm-6">
                <div class="form-group">
        """
        for schedulemember in schedule.schedulemember_set.all():
            html += """
            <div class="form-check">
                <label class="form-check-label">
                    <input class="form-check-input" value={value} {checked} type="checkbox">{name}
                </label>
            </div>
            """.format(value=schedulemember.membro.id, name=schedulemember.membro.cliente.full_name, checked="checked" if schedulemember.presenca else "")
        html += """
                </div>
            </div>
        </div>
        """
    except:
        return JsonResponse({'data': ""}, status=200)
    return JsonResponse({'data': html}, safe=False, status=200)


def set_presence(request):
    schedule_id = request.POST.get('schedule_id', None)
    presence = json.loads(request.POST.get('presence', '[]'))
    unpresence = json.loads(request.POST.get('unpresence', '[]'))
    try:
        with transaction.atomic(using=get_subdomain(request)):
            if schedule_id:
                schedulemembers = ScheduleMember.objects.filter(escala_id=schedule_id)
                for schedulemember in schedulemembers:
                    if str(schedulemember.membro.id) in presence:
                        schedulemember.presenca = True
                    if str(schedulemember.membro.id) in unpresence:
                        schedulemember.presenca = False
                    schedulemember.save()
                return JsonResponse({"data": "Presença registrada com sucesso!"}, status=200)
            else:
                return JsonResponse({"data": "Escala não Identificada"}, status=404)
    except Exception as exc:
        return JsonResponse({"data": "Erro ao registrar presenca"}, status=500)


def get_schedules_by_member(request, pk):
    member = Member.objects.get(id=pk)
    schedules = Schedule.objects.filter(schedulemember__membro=member)

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
            'obs': schedule.obs,
            'membros': list(schedule.schedulemember_set.all().values_list('membro__cliente__first_name', flat=True))
        })
    return JsonResponse({'data': result}, status=200)


def confirm_presence_api(request):
    player_id = request.POST.get('player_id', '')
    schedule_id = request.POST.get('schedule_id', '')
    lat = request.POST.get('lat', None)
    lng = request.POST.get('lng', None)
    context = {}
    try:
        if lat and lng:
            member = Member.objects.get(cliente__player_id=player_id)
            schedule_member = ScheduleMember.objects.get(escala=schedule_id, membro=member)
            location_active = Location.objects.get(grupo=member.grupo, active=True)
            user_location = (float(lat), float(lng))
            schedule_location = (location_active.latitude, location_active.longitude)

            distance = haversine(user_location, schedule_location, unit=Unit.METERS)
            if distance <= float(100):
                schedule_member.presenca = True
                schedule_member.save()

                context.update({
                    'message': 'Utilizamos sua localização para verificar que você realmente está em <strong>{}</strong> 📍.'.format(location_active.descricao),
                    'title': 'Presença Confirmada 😉',
                    'status': 'success'
                })
            else:
                schedule_member.presenca = False
                schedule_member.save()

                context.update({
                    'message': 'Utilizamos sua localização para verificar que você realmente está em <strong>{}</strong> 📍.'.format(location_active.descricao),
                    'title': 'Parece que você não está no local correto 😔',
                    'status': 'error'
                })
        else:
            context.update({
                'message': 'Não conseguimos identificar sua localização.📍',
                'title': 'Sentimos Muito 😔',
                'status': 'error'
            })
    except (Member.DoesNotExist, Member.MultipleObjectsReturned) as exc:
        context.update({
            'message': 'Não conseguimos identificar seu cadastro no sistema.',
            'title': 'Sentimos Muito 😔',
            'status': 'error'
        })
    except (ScheduleMember.DoesNotExist, ScheduleMember.MultipleObjectsReturned) as exc:
        context.update({
            'message': 'Não conseguimos identificar esta Escala.',
            'title': 'Sentimos Muito 😔',
            'status': 'error'
        })
    return JsonResponse(context, status=200)
