from django import forms


class LoginForm(forms.Form):

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
