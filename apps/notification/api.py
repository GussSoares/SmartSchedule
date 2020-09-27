from django.http import JsonResponse
from ..cliente.models import Member


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
