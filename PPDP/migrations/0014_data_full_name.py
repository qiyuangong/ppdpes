# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-29 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPDP', '0013_anon_algorithm_short'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='full_name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
