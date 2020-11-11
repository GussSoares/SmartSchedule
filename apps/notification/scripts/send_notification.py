import requests
import json
import datetime
import pytz
from django.conf import settings
from apps.escala.models import Schedule
from apps.location.models import Location

timezone = pytz.timezone(settings.TIME_ZONE)
default_ini = timezone.localize(datetime.datetime.now())
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
                    try:
                        grupo = members.using(db).first().membro.grupo
                        location = Location.objects.using(db).get(grupo=grupo, active=True)
                    except Exception as exc:
                        location = None

                    header = get_header()
                    # ====================== Reminding Notification ======================
                    payload = {
                        "app_id": settings.ONESIGNAL_APP_ID,
                        "include_player_ids": player_ids,
                        "contents": {"en": "Você está escalado para hoje às {}h.".format(schedule.inicio.astimezone(timezone).strftime("%H:%M"))},
                        "headings": {"en": "Lembrete da Escala 📅"},
                        "web_push_topic": "{}{}".format(schedule.id, datetime.datetime.strftime(datetime.datetime.now().astimezone(timezone), "%Y%m%d%H%M")),
                        "url": "https://{}.smartschedule.ml/acl/schedule-view/".format(db)
                    }
                    print('\t[{}] - NOTIFY ==> SENDING REMINDING NOTIFICATION {}...'.format(datetime.datetime.now(), player_ids))
                    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
                    print('\t ↳ [STATUS] => {}'.format(str(req)))

                    # ====================== Presence Confirm Notification ======================
                    # Esta precisa ser individual pois cada membro receberá seu player_id na URL da notificação!!
                    if location:
                        for player_id in player_ids:
                            payload.update({
                                "include_player_ids": player_id,
                                "contents": {"en": "Clique aqui para marcar presença na sua escala de {}h.".format(schedule.inicio.astimezone(timezone).strftime("%H:%M"))},
                                "headings": {"en": "Confirme sua Presença! 📅"},
                                "web_push_topic": "{}{}".format(schedule.id, datetime.datetime.strftime(datetime.datetime.now().astimezone(timezone), "%Y%m%d%H%M")),
                                "send_after": datetime.datetime.strftime(schedule.inicio.astimezone(timezone), '%Y-%m-%d %H:%M:%S GMT%z'),
                                "url": "https://{subdomain}.smartschedule.ml/schedule/confirm-presence/?player_id={player_id}&schedule_id={schedule_id}".format(subdomain=db, player_id=player_id, schedule_id=schedule.id)
                            })
                            print('\t[{}] - NOTIFY ==> SENDING CONFIRM PRESENCE NOTIFICATION {}...'.format(datetime.datetime.now(), player_ids))
                            req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
                            print('\t ↳ [STATUS] => {}'.format(str(req)))

                    # todo: salvar log no banco de dados para cada notificacao enviada
                except Exception as exc:
                    print("\t[{}] - ERROR ==> ERROR TO SEND NOTIFICATION: {}".format(datetime.datetime.now(), str(exc)))
        except Exception as exc:
            print("[{}] - ERROR ==> CONNECTION ERROR <{}>".format(datetime.datetime.now(), db))

