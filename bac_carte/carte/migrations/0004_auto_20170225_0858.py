# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-25 08:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0003_auto_20170225_0854'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carte',
            old_name='utilisation',
            new_name='utilisations',
        ),
    ]
