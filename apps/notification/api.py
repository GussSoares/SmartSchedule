from django.http import JsonResponse
from .models import Commentary
from ..cliente.models import Member
from ..core.utils import today, timezone
import datetime


def register_player_id(request):
    try:
        player_id = request.POST.get('player_id')
        member_id = request.POST.get('member_id')
        member = Member.objects.get(id=member_id)
        member.cliente.player_id = player_id
        member.cliente.save()
    except Exception as exc:
        pass
    return JsonResponse({}, status=200)


def create_commentary(request):
    if request.method == 'POST':
        message = request.POST.get('message', None)
        member_id = request.POST.get('member_id', None)
        try:
            commentary = Commentary(
                membro_id=member_id,
                message=message
            )
            commentary.save()
            return JsonResponse({'msg': 'Enviado com Sucesso!'}, status=200)
        except:
            return JsonResponse({'msg': 'Erro ao Enviar!'}, status=500)


def get_commentaries(request):
    # comentarios dos ultimos 15 dias
    result = {}
    for c in Commentary.objects.filter(created_at__gte=today()-datetime.timedelta(days=15), checked=False):
        if result.get(c.created_at.astimezone(timezone).strftime("%d %b. %y")):
            result[c.created_at.astimezone(timezone).strftime("%d %b. %y")].append({
                'message': c.message,
                'id': c.id,
                'member_id': c.membro.id,
                'client_id': c.membro.cliente.id,
                'member': c.membro.cliente.first_name,
                'date': c.created_at.astimezone(timezone).strftime("%d %b. %y"),
                'time': c.created_at.astimezone(timezone).time().strftime("%H:%M"),
            })
        else:
            result[c.created_at.astimezone(timezone).strftime("%d %b. %y")] = [{
                'message': c.message,
                'id': c.id,
                'member_id': c.membro.id,
                'client_id': c.membro.cliente.id,
                'member': c.membro.cliente.first_name,
                'date': c.created_at.astimezone(timezone).strftime("%d %b. %y"),
                'time': c.created_at.astimezone(timezone).time().strftime("%H:%M"),
            }]

    return JsonResponse({'data': result}, status=200)
