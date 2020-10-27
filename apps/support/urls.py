from django.conf.urls import url
from . import views


app_name = 'support'

urlpatterns = [
    url(r'^$', views.support, name="list"),
]
