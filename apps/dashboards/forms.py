from email.policy import default
from django import forms

from django_select2.forms import  Select2Widget, ModelSelect2MultipleWidget, ModelSelect2Widget

from apps.periodos_academicos.models import PeriodoAcademico
from apps.programas.models import Programa
from apps.usuarios.models import Usuario

class FiltroPeriodoProgramaForm(forms.Form):
    ano = forms.ChoiceField(
        widget=Select2Widget(),
        label="Años",
        required=True,
    )
    periodo_academico = forms.ModelMultipleChoiceField(
        queryset=PeriodoAcademico.obtener_todos(),
        widget=ModelSelect2MultipleWidget(
            model=PeriodoAcademico,
            queryset=PeriodoAcademico.obtener_todos(),
            attrs={'data-minimum-input-length': ''},
            search_fields=['ano']
        ),
        label="Periodo académico",
        required=True,
    )
    programa = forms.ModelChoiceField(
        queryset=Programa.obtener_todos(),
        widget=Select2Widget(),
        label="Programa académico",
        required=True,
    )


    def __init__(self, *args, **kwargs):
        id_estudiante = kwargs.pop('id_estudiante', None)
        super().__init__(*args, **kwargs)


        if id_estudiante is None:
            programas = Programa.obtener_activos()
        else:
            programas = Programa.obtener_programas_por_estudiante(id_estudiante)

        anos = PeriodoAcademico.obtener_anos()
        opciones_anos = []
        for ano in anos:
            opciones_anos.append((ano, ano))

        self.fields["periodo_academico"].widget.queryset = PeriodoAcademico.obtener_periodos_academicos_por_ano(self.initial['ano'])
        self.fields["periodo_academico"].queryset = PeriodoAcademico.obtener_periodos_academicos_por_ano(self.initial['ano'])

        self.fields["programa"].queryset = programas
        self.fields["programa"].initial = self.fields["programa"].queryset.first()
        self.fields["ano"].choices = opciones_anos


class FiltroNivelesEvaluacionPorProfesorForm(FiltroPeriodoProgramaForm):

    profesor = forms.ModelChoiceField(
        queryset=Usuario.obtener_profesores(),
        widget=Select2Widget(),
        label="Profesor",
        required=False,
    )
    periodo_academico = forms.ModelMultipleChoiceField(
        queryset=PeriodoAcademico.obtener_todos(),
        widget=Select2Widget(),
        label="Periodo académico",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        id_curso_del_programa = kwargs.pop('id_curso_del_programa', 0)
        super().__init__(*args, **kwargs)
        self.fields["profesor"].queryset = Usuario.obtener_profesores_por_curso_del_programa(id_curso_del_programa)
        self.fields["profesor"].empty_label = 'Ninguno'
        self.fields["profesor"].widget.attrs['data-placeholder'] = self.fields["profesor"].empty_label


class FiltroProgramaForm(forms.Form):
    programa = forms.ModelChoiceField(
        queryset=Programa.obtener_todos(),
        widget=Select2Widget(),
        label="Programa académico",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        id_estudiante = kwargs.pop('id_estudiante', 0)
        super().__init__(*args, **kwargs)

        self.fields["programa"].queryset = Programa.obtener_programas_por_estudiante(id_estudiante)
        self.fields["programa"].initial = self.fields["programa"].queryset.first()


class FiltroCalificacionesPorActividadForm(forms.Form):

    mostrar_actividad = forms.BooleanField(
        required=False,
        label="Mostrar calificaciones por actividad"
    )