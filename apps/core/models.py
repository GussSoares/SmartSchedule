from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

# Create your models here.
class DefaultModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(_("Criado em"), auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(_("Modificado em"), auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


class UsuarioManager(BaseUserManager):
    def _create_user(self, login, email, password, **extra_fields):
        if not login:
            raise ValueError('The given login must be set')
        email = self.normalize_email(email)
        email = email or None
        login = self.model.normalize_username(login)
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(login, email, password, **extra_fields)

    def create_superuser(self, login, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(login, email, password, **extra_fields)