from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

app_name = 'acl'

urlpatterns = [

    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^register/$', views.register, name="register"),
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^confirm/$', views.confirm, name="confirm"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
