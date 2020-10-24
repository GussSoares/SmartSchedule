"""smart_event URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
# Django imports
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls', namespace='blog')),

    # provide the most basic login/logout functionality
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='core/login.html'),
    #     name='core_login'),
    # url(r'^logout/$', auth_views.LogoutView.as_view(), name='core_logout'),

    # enable the admin interface
    # url(r'^admin/', admin.site.urls),
    url(r'^acl/', include('apps.acl.urls', namespace="acl")),

    url(r'^', include('apps.dashboard.urls', namespace="dashboard")),

    url(r'^client/', include('apps.cliente.urls', namespace="client")),

    url(r'^coordinator/', include('apps.cliente.urls', namespace="coordinator")),

    url(r'^member/', include('apps.cliente.urls', namespace="member")),

    url(r'^group/', include('apps.cliente.urls', namespace="group")),

    url(r'^schedule/', include('apps.escala.urls', namespace="schedule")),

    url(r'^notification/', include('apps.notification.urls', namespace="notification")),

    url(r'^support/', include('apps.support.urls', namespace="support")),

    url(r'^location/', include('apps.location.urls', namespace="location")),

    url(r'^OneSignalSDKWorker.js', cache_control(max_age=2592000)(TemplateView.as_view(
      template_name="onesignal/OneSignalSDKWorker.js",
      content_type='application/javascript',
    )), name='OneSignalSDKWorker.js'),

    url(r'^OneSignalSDKUpdaterWorker.js', cache_control(max_age=2592000)(TemplateView.as_view(
      template_name="onesignal/OneSignalSDKUpdaterWorker.js",
      content_type='application/javascript',
    )), name='OneSignalSDKUpdaterWorker.js')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
