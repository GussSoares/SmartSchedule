from django import forms

from apps.cliente.models import Member


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
    membro = forms.ModelMultipleChoiceField(required=True, queryset=Member.objects.all(), widget=forms.SelectMultiple(attrs={
        'class': "form-control select2",
        'multiple': "multiple",
        'data-placeholder': "Selecione os membros",
        'data-dropdown-css-class': "select2-primary"
    }))

    def __init__(self, *args, **kwargs):
        grupo = kwargs.pop('grupo', None)
        super(CreateScheduleForm, self).__init__(*args, **kwargs)
        if grupo:
            self.fields['membro'].queryset = Member.objects.filter(grupo=grupo)
