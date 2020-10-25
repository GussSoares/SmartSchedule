from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import ScheduleMember
from ..cliente.models import Coordinator, Member
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
    player_id = request.GET.get('player_id', '')
    schedule_id = request.GET.get('schedule_id', '')
    context = {
        'player_id': player_id,
        'schedule_id': schedule_id
    }

    try:
        member = Member.objects.get(cliente__player_id=player_id)
        schedule_member = ScheduleMember.objects.get(escala=schedule_id, membro=member)
        context.update({
            'schedulemember_id': schedule_member.id,
            'message': 'Utilizamos sua localização para verificar que você realmente está em <strong>{}</strong> 📍.'.format('Paróquia Imaculada Conceição'),
            'title': 'Presença Confirmada 😉',
            'status': 'success'
        })
    except (Member.DoesNotExist, Member.MultipleObjectsReturned) as exc:
        context.update({
            'schedulemember_id': None,
            'message': 'Não conseguimos identificar seu cadastro no sistema.',
            'title': 'Sentimos Muito 😔',
            'status': 'error'
        })
    except (ScheduleMember.DoesNotExist, ScheduleMember.MultipleObjectsReturned) as exc:
        context.update({
            'schedulemember_id': None,
            'message': 'Não conseguimos identificar esta Escala.',
            'title': 'Sentimos Muito 😔',
            'status': 'error'
        })

    return render(request, 'confirmar_presenca/confirmar_presenca.html', context)
