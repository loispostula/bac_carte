# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 07:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0004_auto_20170225_0858'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carte',
            old_name='price',
            new_name='prix',
        ),
    ]
