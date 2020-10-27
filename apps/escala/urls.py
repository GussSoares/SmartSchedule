from django.conf.urls import url
from . import views, api


app_name = 'escala'
urlpatterns = [
    url(r'^create/$', views.create, name="create"),
    url(r'^confirm-presence/$', views.confirmar_presenca, name="confirm_presence"),

    url(r'^api/create/$', api.create_schedule, name="api_create"),
    url(r'^api/update/(?P<pk>\d+)$', api.update_schedule, name="api_update"),
    url(r'^api/delete/(?P<pk>\d+)$', api.delete_schedule, name="api_delete"),
    url(r'^api/get-all-schedules/$', api.get_all_schedules, name="get_all_schedules"),
    url(r'^api/get-schedules-by-member/(?P<pk>\d+)$', api.get_schedules_by_member, name="get_schedules_by_member"),
    url(r'^api/get-member-by-schedule/$', api.get_member_by_schedule, name="get_member_by_schedule"),
    url(r'^api/get-member-by-schedule-html-form/$', api.get_member_by_schedule_html_form, name="get_member_by_schedule_html_form"),
    url(r'^api/set-presence/$', api.set_presence, name="set_presence"),
    url(r'^api/confirm-presence/$', api.confirm_presence_api, name="confirm_presence_api"),

    # criado especialmente para o dhxscheduler
    url(r'^create/api/get-member-by-schedule/$', api.get_member_by_schedule, name="get_member_by_schedule"),
]

