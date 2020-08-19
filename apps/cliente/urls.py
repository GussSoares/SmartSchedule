from django.conf.urls import url
from . import views

app_name = "cliente"

urlpatterns = [

    url(r'^create/$', views.create, name="create"),
    url(r'^update/(?P<pk>\d+)$', views.update, name="update"),
    url(r'^set-password/(?P<pk>\d+)$', views.set_password, name="set_password")
]
