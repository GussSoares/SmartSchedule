from django.conf.urls import url
from . import api

app_name = "notification"

urlpatterns = [
    # ---------------------- NOTIFICATION ---------------------- #
    url(r'^register-player-id/$', api.register_player_id, name="register_player_id"),
]
