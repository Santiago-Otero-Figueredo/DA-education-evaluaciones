# Generated by Django 3.2.15 on 2022-09-19 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluaciones', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='nombre',
            field=models.TextField(verbose_name='Nombre de la evaluación'),
        ),
        migrations.AlterField(
            model_name='tipoactividad',
            name='nombre',
            field=models.TextField(verbose_name='Nombre de la actividad de evaluación'),
        ),
    ]
