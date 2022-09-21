from pyexpat import model
from django import forms
from django_select2.forms import ModelSelect2Widget

from apps.programas.models import Programa

class FiltroPrograma(forms.Form):

    programas = forms.ModelChoiceField(
        queryset=Programa.obtener_todos(),
        widget=ModelSelect2Widget(
            model=Programa,
            attrs={'data-minimum-input-length': ''},
            search_fields=['nombre', 'codigo']
        ),
        label="Programa académico",
        required=True,
    )

    def __init__(self, *args, **kwargs) -> None:
        programas_del_profesor = kwargs.pop('programas', Programa.objects.none())
        super().__init__(*args, **kwargs)

        self.fields['programas'].queryset = programas_del_profesor
        self.fields['programas'].widget.queryset = programas_del_profesor