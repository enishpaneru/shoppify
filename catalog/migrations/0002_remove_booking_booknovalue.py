# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 11:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='booknovalue',
        ),
    ]
