from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from apps.cliente.models import Coordinator
from apps.core.utils import get_subdomain
from apps.escala.models import Schedule
from apps.location.models import Location


@csrf_exempt
def get_all_api(request):
    if request.user.is_coordinator:
        group = Coordinator.objects.get(cliente=request.user).grupo
        locations = Location.objects.filter(grupo=group)
    elif request.user.is_superuser:
        locations = Location.objects.all()
    else:
        locations = []
    result = []
    for location in locations:
        result.append({
            'id': location.id,
            'descricao': location.descricao,
            'latitude': location.latitude,
            'longitude': location.longitude
        })
    return JsonResponse({'data': result})


@csrf_exempt
def create_api(request):
    latitude = request.POST.get('latitude', None)
    longitude = request.POST.get('longitude', None)
    descricao = request.POST.get('descricao', None)
    active = True if request.POST.get('active', False) == 'true' else False
    group = None
    if request.user.is_coordinator:
        group = Coordinator.objects.get(cliente=request.user).grupo

    if latitude and longitude:
        try:
            if active:
                Location.objects.filter(grupo=group).update(active=False)
            location = Location.objects.create(
                latitude=float(latitude),
                longitude=float(longitude),
                descricao=descricao,
                grupo=group,
                active=active
            )
            location_json = {
                'id': location.id,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'descricao': location.descricao
            }
        except Exception as exc:
            return JsonResponse({'msg': 'Erro ao salvar localização!'}, status=500)
        return JsonResponse({'msg': 'Localização salva com sucesso!', 'data': location_json}, status=200)
    return JsonResponse({'msg': 'Latitude e Longitude não informados'}, status=500)


@csrf_exempt
def update_api(request, pk):
    try:
        location = get_object_or_404(Location, pk=pk)
        descricao = request.POST.get('descricao', None)
        location.descricao = descricao
        location.save()
        location_json = {
            'id': location.id,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'descricao': location.descricao
        }
    except Exception as exc:
        return JsonResponse({'msg': 'Erro ao atualizar localização!'}, status=500)
    return JsonResponse({'msg': 'Localização atualizada com sucesso!', 'data': location_json}, status=200)


@csrf_exempt
def delete_api(request, pk):
    try:
        get_object_or_404(Location, pk=pk).delete()
    except Exception as exc:
        return JsonResponse({'msg': 'Erro ao deletar localização!'}, status=500)
    return JsonResponse({'msg': 'Localização deletada com sucesso!'}, status=200)


@csrf_exempt
def active_api(request, pk):
    try:
        with transaction.atomic(using=get_subdomain(request)):
            location = get_object_or_404(Location, pk=pk)

            # tenta desativar todas as outras localizacoes para manter a concistencia
            try:
                grupo = location.grupo
                Location.objects.filter(grupo=grupo).update(active=False)
            except:
                pass
            location.active = True
            location.save()
    except Exception as exc:
        return JsonResponse({'msg': 'Erro ao ativar localização!'}, status=500)
    return JsonResponse({'msg': 'Localização ativada com sucesso!'}, status=200)
