from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

app_name = "cliente"

urlpatterns = [

    url(r'^create/$', views.create, name="create"),
    url(r'^update/(?P<pk>\d+)$', views.update, name="update"),
    url(r'^set-password/(?P<pk>\d+)$', views.set_password, name="set_password"),
    url(r'^delete/(?P<pk>\d+)$', views.delete, name="delete")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
