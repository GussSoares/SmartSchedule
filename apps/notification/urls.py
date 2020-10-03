from django.conf.urls import url
from . import api

app_name = "notification"

urlpatterns = [
    # ---------------------- NOTIFICATION ---------------------- #
    url(r'^register-player-id/$', api.register_player_id, name="register_player_id"),

    # ---------------------- COMMENTARY ------------------------ #
    url(r'^create-commentary/$', api.create_commentary, name="create_commentary"),

    # -------------------- API COMMENTARY ---------------------- #
    url(r'^get-commentaries/$', api.get_commentaries, name="get_commentaries")
]
