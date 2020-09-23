from django import forms
from .models import Client, Group, Coordinator, Member
from ..core.forms import CustomForm, CustomModelForm


class ClientForm(CustomModelForm):

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'login', 'email', 'cpf_cnpj', 'data_nascimento', 'telefone', 'cep',
                  'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'foto']
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
            'cpf_cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CPF',
                'autocomplete': 'off'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': '__/__/__',
                'autocomplete': 'off'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefone',
                'autocomplete': 'off'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CEP',
                'autocomplete': 'off'
            }),
            'logradouro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço',
                'autocomplete': 'off'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número',
                'autocomplete': 'off'
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Complemento',
                'autocomplete': 'off'
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bairro',
                'autocomplete': 'off'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade',
                'autocomplete': 'off'
            }),
            'uf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UF',
                'autocomplete': 'off'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'style': 'display: none'
            })
        }


class SetPasswordForm(CustomForm):

    password1 = forms.CharField(required=True, localize=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Senha'
    }))
    password2 = forms.CharField(required=True, localize=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirme a Senha'
    }))


class CoordForm(CustomModelForm):
    class Meta:
        model = Coordinator
        fields = ['grupo']
        widgets = {
            'grupo': forms.Select(attrs={
                'class': 'form-control select2',
                'placeholder': 'Informe uma Grupo'
            })
        }


class MemberForm(CustomModelForm):
    class Meta:
        model = Member
        fields = ['grupo']
        widgets = {
            'grupo': forms.Select(attrs={
                'class': 'form-control select2',
                'placeholder': 'Informe uma Grupo'
            })
        }


class GroupForm(CustomModelForm):

    class Meta:
        model = Group
        fields = ['descricao']
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Informe uma Descrição'
            })
        }
