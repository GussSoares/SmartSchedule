from django import forms
from apps.cliente.models import Group


class CreateLocationForm(forms.Form):
    grupo = forms.ModelChoiceField(required=True, queryset=None, widget=forms.Select(attrs={
        'class': "form-control select2",
        'data-placeholder': "Selecione um grupo",
        'data-dropdown-css-class': "select2-primary"
    }))

    def __init__(self, *args, **kwargs):
        super(CreateLocationForm, self).__init__(*args, **kwargs)
        self.fields['grupo'].queryset = Group.objects.all()
