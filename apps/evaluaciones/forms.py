from dataclasses import fields
from pyexpat import model
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from django_select2.forms import ModelSelect2Widget
from apps.evaluaciones.models import Nota, CalificacionCualitativa, Pregunta
from apps.usuarios.models import Usuario


class PreguntaEstudianteForm(forms.Form):

    def __init__(self, *arg, **kwargs):
        self.estudiantes = kwargs.pop('estudiantes', Usuario.objects.none())
        self.preguntas = kwargs.pop('preguntas', Pregunta.objects.none())

        super().__init__(*arg, **kwargs)



    def get_nota(self):
        if self.pregunta is not None and self.estudiante is not None:
            return Nota.obtener_por_estudiante_y_pregunta(self.estudiante.pk, self.pregunta.pk)




class NotaEstudianteCualitativoForm(PreguntaEstudianteForm):

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        for estudiante in self.estudiantes:
            for pregunta in self.preguntas:
                self.fields[f'{estudiante.pk}-{pregunta.pk}'] = forms.ModelChoiceField(
                                            queryset=CalificacionCualitativa.obtener_todos(),
                                            widget=forms.Select(attrs={
                                                    'class': "form-select"
                                                }
                                            ),
                                            required=True
                                        )
                self.fields[f'{estudiante.pk}-{pregunta.pk}'].empty_label = f'Pregunta #{pregunta.numeracion}'



class NotaEstudianteCuantitativoForm(PreguntaEstudianteForm):

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        for estudiante in self.estudiantes:
            for pregunta in self.preguntas:
                self.fields[f'{estudiante.pk}-{pregunta.pk}'] = forms.FloatField(
                                            validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
                                            widget=forms.NumberInput(attrs={
                                                    'placeholder': f'Pregunta #{pregunta.numeracion}',
                                                    'class': "form-control"
                                                }
                                            ),
                                            required=True

                                        )

