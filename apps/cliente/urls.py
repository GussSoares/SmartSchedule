from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

app_name = "cliente"

urlpatterns = [
    # ---------------------- CLIENTE ---------------------- #
    url(r'^create-client/$', views.create_cliente, name="create_client"),
    url(r'^update-client/(?P<pk>\d+)$', views.update_cliente, name="update_client"),
    url(r'^set-password/(?P<pk>\d+)$', views.set_password, name="set_password"),
    url(r'^delete-client/(?P<pk>\d+)$', views.delete_cliente, name="delete_client"),

    # -------------------- COORDENADOR -------------------- #
    url(r'^create-coord/$', views.create_coord, name="create_coord"),
    url(r'^update-coord/(?P<pk>\d+)$', views.update_coord, name="update_coord"),
    url(r'^delete-coord/(?P<pk>\d+)$', views.delete_coord, name="delete_coord"),

    # ---------------------- MEMBRO ---------------------- #
    url(r'^create-member/$', views.create_membro, name="create_member"),
    url(r'^update-member/(?P<pk>\d+)$', views.update_membro, name="update_member"),
    url(r'^update-member/(?P<pk>\d+)/(?P<comment_id>\d+)$', views.update_membro, name="update_member_comment"),
    url(r'^delete-member/(?P<pk>\d+)$', views.delete_membro, name="delete_member"),

    # ---------------------- GRUPO ---------------------- #
    url(r'^create-group/$', views.create_grupo, name="create_group"),
    url(r'^update-group/(?P<pk>\d+)$', views.update_grupo, name="update_group"),
    url(r'^delete-group/(?P<pk>\d+)$', views.delete_grupo, name="delete_group"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
