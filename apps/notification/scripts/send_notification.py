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


def run(*args):
    print("[{}] - RUN ==> Running Script Send Notifications...".format(datetime.datetime.now()))
    print("\n")
    for db, conf_db in settings.DATABASES.items():
        try:
            print("[{}] - TRY ==> ACCESSING DATABASE <{}>...".format(datetime.datetime.now(), db))
            schedules = Schedule.objects.using(db).filter(inicio__gte=default_ini, fim__lte=default_end)

            for schedule in schedules:
                try:
                    members = schedule.schedulemember_set.using(db).all()
                    player_ids = list(members.values_list('membro__cliente__player_id', flat=True))

                    header = get_header()
                    payload = {
                        "app_id": settings.ONESIGNAL_APP_ID,
                        "include_player_ids": player_ids,
                        "contents": {"en": "Você está escalado para hoje às {}h.".format(schedule.inicio.astimezone(timezone).strftime("%H:%M"))},
                        "headings": {"en": "Eai! Cuida na Escala. 📅"},
                        "web_push_topic": schedule.id,
                        "url": "https://{}.smartschedule.ml/acl/login-confirm".format(db)
                    }
                    print('\t[{}] - NOTIFY ==> SENDING NOTIFICATION {}...'.format(datetime.datetime.now(), player_ids))
                    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
                    print(req)

                    # todo: salvar log no banco de dados para cada notificacao enviada
                except Exception as exc:
                    print("\t[{}] - ERROR ==> ERROR TO SEND NOTIFICATION: {}".format(datetime.datetime.now(), str(exc)))
        except Exception as exc:
            print("[{}] - ERROR ==> CONNECTION ERROR <{}>".format(datetime.datetime.now(), db))

