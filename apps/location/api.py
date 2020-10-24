from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from apps.cliente.models import Coordinator
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
    group = None
    if request.user.is_coordinator:
        group = Coordinator.objects.get(cliente=request.user).grupo

    if latitude and longitude:
        try:
            location = Location.objects.create(
                latitude=float(latitude),
                longitude=float(longitude),
                descricao=descricao,
                grupo=group
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
