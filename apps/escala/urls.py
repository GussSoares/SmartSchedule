from django.conf.urls import url
from . import views, api


app_name = 'escala'

urlpatterns = [
    url(r'^create/$', views.create, name="create"),

    url(r'^api/create/$', api.create_schedule, name="api_create"),
    url(r'^api/update/(?P<pk>\d+)$', api.update_schedule, name="api_update"),
    url(r'^api/get-all-schedules/$', api.get_all_schedules, name="get_all_schedules"),
]
