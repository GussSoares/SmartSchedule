from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext as _
from ..core.models import DefaultModel, UsuarioManager


# Create your models here.
class Cliente(DefaultModel, PermissionsMixin, AbstractBaseUser):

    login = models.CharField(_("Login"), max_length=50, unique=True)
    first_name = models.CharField(_("Primeiro Nome"), max_length=50)
    last_name = models.CharField(_("Último Nome"), max_length=50, null=True, blank=True)
    email = models.EmailField(_("Email"), max_length=254, null=True, blank=True)
    cpf_cnpj = models.CharField(_("CPF/CNPJ"), max_length=14, null=True, blank=True)
    telefone = models.CharField(_("Telefone"), max_length=13, null=True, blank=True)
    is_active = models.BooleanField(_("Ativo"), default=True, null=False, blank=True)
    logradouro = models.CharField(_("Endereço"), max_length=255, null=True, default=None, blank=True)
    numero = models.CharField(_("Número"), max_length=255, null=True, default=None, blank=True)
    complemento = models.CharField(_("Complemento"), max_length=255, null=True, default=None, blank=True)
    cep = models.CharField(_("CEP"), max_length=255, null=True, default=None, blank=True)
    bairro = models.CharField(_("Bairro"), max_length=255, null=True, default=None, blank=True)
    cidade = models.CharField(_("Cidade"), max_length=255, null=True, default=None, blank=True)
    uf = models.CharField(_("UF"), max_length=255, null=True, default=None, blank=True)
    data_nascimento = models.DateField(_("Data de Nascimento"), null=True, blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'login'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def full_address(self):
        return "{} {} {} {} {} {}".format(self.logradouro, self.numero, self.complemento, self.bairro, self.cidade,
                                          self.uf)

    @property
    def full_address_humanized(self):
        return"{} {} - {}, {}, {} - {}".format(self.logradouro or "", self.numero or "", self.complemento or "",
                                               self.bairro or "", self.cidade or "", self.uf or "")
