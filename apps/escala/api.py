from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from ..escala.forms import CreateScheduleForm
import datetime


@csrf_exempt
def create_schedule(request):
    # form = CreateScheduleForm()
    # if request.method == 'POST':
    #     form = CreateScheduleForm(request.POST)
    #     if form.is_valid():
    #         # convert time in timedelta
    #         start = datetime.datetime.combine(form.cleaned_data.get('data'), form.cleaned_data.get('hora'))
    #         end = start + datetime.timedelta(hours=1)
    #
    #         schedule = {
    #             'id': 1,
    #             'title': form.cleaned_data.get('nome'),
    #             'calendarId': 1,
    #             'start': start,
    #             'end': end
    #         }
    #         return JsonResponse({'schedule': schedule}, status=200)
    #
    # context = {
    #     'form': form
    # }
    schedule = {
        'id': 1,
        'title': request.POST.get('title'),
        'calendarId': 1,
        'start': request.POST.get('start'),
        'end': request.POST.get('end')
    }
    return JsonResponse({'schedule': schedule}, status=200)
    # return render(request, 'escala/modals/create.html', context)


@csrf_exempt
def update_schedule(request, pk):
    # schedule = get_object_or_404()
    form = CreateScheduleForm(data={
        'id': 1,
        'title': 'lalalla',
        'calendarId': 1,
        'start': datetime.datetime.now(),
        'end': datetime.datetime.now()
    })
    if request.method == 'POST':
        form = CreateScheduleForm(request.POST)
        if form.is_valid():
            # convert time in timedelta
            start = datetime.datetime.combine(form.cleaned_data.get('data'), form.cleaned_data.get('hora'))
            end = start + datetime.timedelta(hours=1)

            schedule = {
                'id': 1,
                'title': form.cleaned_data.get('nome'),
                'calendarId': 1,
                'start': start,
                'end': end
            }
            return JsonResponse({'schedule': schedule}, status=200)

    context = {
        'form': form
    }
    return render(request, 'escala/modals/create.html', context)


def get_all_schedules(request):
    return JsonResponse({'data': [
        {
            'id': '1',
            'text': 'lalala',
            'category': 'time',
            'calendarId': '1',
            'start_date': datetime.datetime.now(),
            'end_date': datetime.datetime.now(),
            'user_id': '1,2,3'
        },
        {
            'id': '2',
            'text': 'lalala',
            'category': 'time',
            'calendarId': '1',
            'start_date': datetime.datetime.now(),
            'end_date': datetime.datetime.now()
        },
        {
            'id': '3',
            'text': 'lalala',
            'category': 'time',
            'calendarId': '1',
            'start_date': datetime.datetime.now(),
            'end_date': datetime.datetime.now()
        },
        {
            'id': '4',
            'text': 'lalala',
            'category': 'time',
            'calendarId': '1',
            'start_date': datetime.datetime.now(),
            'end_date': datetime.datetime.now()
        },
    ]}, status=200)
