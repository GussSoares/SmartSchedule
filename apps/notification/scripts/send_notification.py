import argparse
import requests
import json
import datetime
import pytz
from django.conf import settings
from apps.escala.models import Schedule

timezone = pytz.timezone(settings.TIME_ZONE)
default_ini = timezone.localize(datetime.datetime.now().replace(hour=0, minute=0, second=0))
default_end = timezone.localize(datetime.datetime.now().replace(hour=23, minute=59, second=59))


def get_header():
    return {"Content-Type": "application/json; charset=utf-8"}


def get_payload(player_ids, title, message, schedule_id):
    return {"app_id": settings.ONESIGNAL_APP_ID,
            "include_player_ids": player_ids,
            "contents": {"en": message},
            "headings": {"en": title},
            "web_push_topic": schedule_id,
            "url": "https://teste.smartschedule.ml/acl/login-confirm"
            }


def run(*args):
    print("[{}] - RUN ==> Running Script Send Notifications...".format(datetime.datetime.now()))
    schedules = Schedule.objects.filter(inicio__gte=default_ini, fim__lte=default_end)

    for schedule in schedules:
        try:
            members = schedule.schedulemember_set.all()
            player_ids = list(members.values_list('membro__cliente__player_id', flat=True))

            msg = "Você está escalado para hoje às {}h.".format(schedule.inicio.astimezone(timezone).strftime("%H:%M"))
            title = "Eai! Cuida na Escala. 📅"
            header = get_header()
            # payload = get_payload(['5d10d117-f413-4cee-82c5-5724bd949125'], title, msg)
            payload = get_payload(player_ids, title, msg, schedule.id)
            print('[{}] - NOTIFY ==> Sending Notification to {}...'.format(datetime.datetime.now(), player_ids))
            req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
            print(req)

            # todo: salvar log no banco de dados para cada notificacao enviada
        except Exception as exc:
            print("[{}] - ERROR ==> Erro ao enviar notificacao: {}".format(datetime.datetime.now(), str(exc)))


