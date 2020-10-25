from django.conf.urls import url
from . import views, api


app_name = 'location'

urlpatterns = [
    url(r'^create/$', views.create, name="create"),

    # API
    url(r'^api/create/$', api.create_api, name="create_api"),
    url(r'^api/update/(?P<pk>\d+)$', api.update_api, name="update_api"),
    url(r'^api/delete/(?P<pk>\d+)$', api.delete_api, name="delete_api"),
    url(r'^api/active/(?P<pk>\d+)$', api.active_api, name="active_api"),
    url(r'^api/get-all-locations/$', api.get_all_api, name="get_all_locations"),
]
