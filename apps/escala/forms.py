from django import forms


class CreateScheduleForm(forms.Form):
    nome = forms.CharField(required=True, localize=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nome'
    }))
    data = forms.DateField(required=True, localize=True, widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'Data',
        'type': 'date'
    }))
    hora = forms.TimeField(required=True, localize=True, widget=forms.TimeInput(attrs={
        'class': 'form-control',
        'placeholder': 'Hora',
        'type': 'time'
    }))
