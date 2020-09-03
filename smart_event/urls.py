"""smart_event URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
# Django imports
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
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

    url(r'^cliente/', include('apps.cliente.urls', namespace="cliente"))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
