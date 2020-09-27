from django import forms
from ..core.forms import CustomModelForm, CustomForm
from ..cliente.models import Client


class LoginForm(CustomForm):

    login = forms.CharField(max_length=255, required=True, localize=True,
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Login'
                            }))

    password = forms.CharField(max_length=255, required=True, localize=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Password'
                               }))


class RegisterForm(CustomModelForm):

    error_css_class = 'is-invalid'

    password1 = forms.CharField(required=True, localize=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Senha'
    }))
    password2 = forms.CharField(required=True, localize=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirme a Senha'
    }))

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'login', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome',
                'autocomplete': 'off'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sobrenome',
                'autocomplete': 'off'
            }),
            'login': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Login',
                'autocomplete': 'off'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'autocomplete': 'off'
            }),
        }


class LoginConfirmForm(CustomForm):

    cpf = forms.CharField(max_length=255, required=True, localize=True,
                          widget=forms.TextInput(attrs={
                              'class': 'form-control',
                              'placeholder': 'CPF'
                          }))
