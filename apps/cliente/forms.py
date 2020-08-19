from django import forms
from django.core.exceptions import ValidationError

from .models import Cliente


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['first_name', 'last_name', 'login', 'email', 'cpf_cnpj', 'data_nascimento', 'telefone', 'cep',
                  'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf']
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
        }


class SetPasswordForm(forms.Form):

    password1 = forms.CharField(required=True, localize=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Senha'
    }))
    password2 = forms.CharField(required=True, localize=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirme a Senha'
    }))

    def clean(self):
        cleaned_data = super(SetPasswordForm, self).clean()

        if 'password1' in self.changed_data and 'password2' in self.changed_data:
            if cleaned_data.get('password1') == cleaned_data.get('password2'):
                return cleaned_data
            else:
                self.add_error('password1', ValidationError("As senhas não coicidem!"))

        return cleaned_data
