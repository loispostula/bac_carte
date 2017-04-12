# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-25 08:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0002_auto_20170225_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='carte',
            name='price',
            field=models.FloatField(blank=True, help_text='Prix', null=True),
        ),
        migrations.AlterField(
            model_name='carte',
            name='compositions',
            field=models.ManyToManyField(blank=True, help_text='Composition', through='carte.Composition', to='carte.Composant'),
        ),
        migrations.AlterField(
            model_name='carte',
            name='images',
            field=models.ManyToManyField(blank=True, help_text="Pictogramme d'information", to='carte.TissuImage'),
        ),
        migrations.AlterField(
            model_name='carte',
            name='utilisation',
            field=models.ManyToManyField(blank=True, help_text='Utilisation', to='carte.Utilisation'),
        ),
    ]
