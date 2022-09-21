from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from django_select2.forms import ModelSelect2Widget
from apps.evaluaciones.models import Nota, CalificacionCualitativa, Pregunta

class PreguntaEstudianteForm(forms.ModelForm):

    def __init__(self, *arg, **kwargs):
        self.estudiante = kwargs.pop('estudiante', None)

        super().__init__(*arg, **kwargs)

        self.pregunta = self.instance

        self.empty_permitted = False
        for _, field in self.fields.items():
            field.widget.attrs['required'] = 'required'


    def get_nota(self):
        if self.pregunta is not None and self.estudiante is not None:
            return Nota.obtener_por_estudiante_y_pregunta(self.estudiante.pk, self.pregunta.pk)

    class Meta:
        model = Pregunta
        fields = ('numeracion', )
        widgets = {
            'numeracion': forms.TextInput(attrs={'type': 'hidden'}),
        }



class NotaEstudianteCualitativoForm(PreguntaEstudianteForm):

    calificacion_cualitativa = forms.ModelChoiceField(
        queryset=CalificacionCualitativa.obtener_todos(),
        required=True
    )

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        if self.get_nota():
            self.fields['calificacion_cualitativa'].initial = self.get_nota().calificacion_cualitativa


class NotaEstudianteCuantitativoForm(PreguntaEstudianteForm):

    resultado = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        required=True
    )

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        if self.get_nota():
            self.fields['resultado'].initial = self.get_nota().resultado



notas_cualitativas_formset = forms.modelformset_factory(Pregunta, form=NotaEstudianteCualitativoForm, extra=0)
notas_cuantitativas_formset = forms.modelformset_factory(Pregunta, form=NotaEstudianteCuantitativoForm, extra=0)
